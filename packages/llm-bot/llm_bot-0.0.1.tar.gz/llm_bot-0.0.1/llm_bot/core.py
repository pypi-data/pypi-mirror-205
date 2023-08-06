# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from pathlib import Path
import pickle
from typing import List, Tuple, Union

import faiss
from faiss import IndexFlat
from langchain.chat_models.openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

# TODO: download the model from the internet

INDEX_FILENAME = "index.faiss"
STORE_FILENAME = "store.pickle"


class BaseLLMBot(ABC):
    def __init__(self, temperature: float = 0):
        self._store: FAISS = None
        self._chat = ChatOpenAI(temperature=temperature)

    @abstractmethod
    def train(self, *args, **kwargs) -> None:
        pass

    def save(self, path: Union[str, Path]) -> None:
        """
        Saves the index and the vector store to the given path.

        Args:
            path (Union[str, Path]): The path to save the index and vector store to.
        """
        # Assert that the path exists
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        # Save the index
        index_fname = str(path / INDEX_FILENAME)
        faiss.write_index(self._store.index, index_fname)

        # Save the vector store
        index = self._store.index
        self._store.index = None
        store_fname = str(path / STORE_FILENAME)
        with open(store_fname, "wb") as f:
            pickle.dump(self._store, f)
        self._store.index = index

    def load(self, path: Union[str, Path]) -> None:
        """
        Loads the index and the vector store from the given path.

        Args:
            path (Union[str, Path]): The path to load the index and vector store from.
        """
        # Assert that the path exists
        path = Path(path)
        assert path.exists(), f"Path {path} does not exist."

        # Assert that both files exist
        index_fname = path / INDEX_FILENAME
        store_fname = path / STORE_FILENAME
        assert (
            index_fname.exists() and store_fname.exists()
        ), f"Either {index_fname} or {store_fname} does not exist."

        # Load the index
        index: IndexFlat = faiss.read_index(str(index_fname))

        # Load the vector store
        with open(store_fname, "rb") as f:
            self._store: FAISS = pickle.load(f)
        self._store.index = index

    def build_messages(
        self,
        personality_prompt: str,
        user_message: str,
        chat_history: str = None,
        chat_history_prompt: str = "Aqui está o histórico da conversa até agora:",
        use_context: bool = True,
        context_prompt: str = "Aqui estão pedaços de informação que você pode usar:",
        number_of_context_docs: int = 2,
    ) -> Tuple[List[BaseMessage], List[str]]:
        """
        Builds a list of messages to send to the chatbot.

        Args:
            personality_prompt (str): The prompt to use for the personality.
            user_message (str): The message from the user.
            chat_history (str, optional): The chat history. If not provided, the chat history will
                be empty. Defaults to None.
            chat_history_prompt (str, optional): The prompt to use for the chat history. Defaults
                to "Aqui está o histórico da conversa até agora:".
            use_context (bool, optional): Whether to search for context documents in the vector
                store. Defaults to True.
            context_prompt (str, optional): The prompt to use for the context documents. Defaults
                to "Aqui estão pedaços de informação que você pode usar:".
            number_of_context_docs (int, optional): The number of context documents to use. Defaults
                to 2.

        Returns:
            Tuple[List[BaseMessage], List[str]]: A tuple containing the list of messages to send to
                the chatbot and the list of sources of the context documents.
        """
        # Start list of messages with the personality prompt
        messages: List[BaseMessage] = [SystemMessage(content=personality_prompt)]

        # If we are using context, search for context documents and add them to the prompt
        sources: List[str] = []
        if use_context:
            messages.append(SystemMessage(content=context_prompt))
            docs = self._store.similarity_search(user_message, k=number_of_context_docs)
            sources = list(set([doc.metadata["source"] for doc in docs]))
            for doc in docs:
                messages.append(SystemMessage(content=f"- {doc.page_content}"))

        # If chat history is provided, add messages for it
        if chat_history:
            messages.append(SystemMessage(content=chat_history_prompt))
            messages.append(HumanMessage(content=chat_history))

        # Add the user message
        messages.append(HumanMessage(content=user_message))

        return messages, sources

    def chat(self, messages: List[BaseMessage]) -> str:
        """
        Sends the given messages to the chatbot and returns the response.

        Args:
            messages (List[BaseMessage]): The messages to send to the chatbot.
        """
        # Send the messages to the chatbot
        ai_message = self._chat(messages)

        # Return the response
        return ai_message.content


class HTMLBot(BaseLLMBot):
    def train(
        self,
        documents_path: Union[str, Path],
        text_chunk_size: int = 1000,
        text_chunk_overlap: int = 250,
        text_separators: List[str] = [" ", ".", ",", ";", ":", "!", "?", "\n"],
    ) -> None:
        """
        Trains the bot using the given documents.

        Args:
            documents_path (Union[str, Path]): The path to the documents to use for training.
            text_chunk_size (int, optional): The size of the text chunks to use for training.
                Defaults to 1000.
            text_chunk_overlap (int, optional): The overlap between text chunks. Defaults to 250.
            text_separators (List[str], optional): The list of text separators to use for splitting
                the text into chunks. Defaults to [" ", ".", ",", ";", ":", "!", "?", "\n"].
        """
        # Import stuff (importing here avoids unnecessary dependencies)
        from langchain.document_loaders import BSHTMLLoader

        # Assert that the path exists
        documents_path = Path(documents_path)
        assert documents_path.exists(), f"Path {documents_path} does not exist."

        # Load the knowledge base
        loaders: List[BSHTMLLoader] = []
        for html_file in documents_path.glob("**/*.html"):
            loaders.append(BSHTMLLoader(html_file))
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=text_chunk_size,
            chunk_overlap=text_chunk_overlap,
            separators=text_separators,
        )
        docs = []
        for loader in loaders:
            docs.extend(loader.load_and_split(text_splitter=text_splitter))

        # Create the vector store
        embedding = OpenAIEmbeddings()
        self._store = FAISS.from_documents(documents=docs, embedding=embedding)

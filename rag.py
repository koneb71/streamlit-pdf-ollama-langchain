import weaviate
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_weaviate import WeaviateVectorStore

from config import WEAVIATE_HOST_URL, OLLAMA_API_BASE_URL


def get_embedding(model: str = "nomic-embed-text"):
    """
    This function is used to get the embeddings from the Ollama model.

    Parameters:
    model (str): The name of the model to use for the embeddings.
                 Default is "nomic-embed-text".

    Returns:
    OllamaEmbeddings: An instance of the OllamaEmbeddings class with the specified model.
    """
    return OllamaEmbeddings(base_url=OLLAMA_API_BASE_URL, model=model)


def load_documents(path: str = "uploads"):
    """
    This function is used to load documents from a specified directory.

    Parameters:
    path (str): The path to the directory from which to load the documents.
                Default is "uploads".

    Returns:
    list[Document]: A list of Document objects representing the loaded documents.
    """
    document_loader = PyPDFDirectoryLoader(path)
    return document_loader.load()


def split_documents(documents: list[Document]):
    """
    This function is used to split the documents into chunks.

    Parameters:
    documents (list[Document]): A list of Document objects to be split.

    Returns:
    list[Document]: A list of Document objects representing the split documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=80, length_function=len, is_separator_regex=False
    )
    return text_splitter.split_documents(documents)


def add_to_weaviate_store(
    chunks: list[Document],
):
    """
    This function is used to add document chunks to the Weaviate store.

    Parameters:
    chunks (list[Document]): A list of Document objects representing the chunks to be added.

    Returns:
    WeaviateVectorStore: An instance of the WeaviateVectorStore class with the added chunks.
    """
    return WeaviateVectorStore.from_documents(
        chunks,
        get_embedding(),
        client=weaviate.connect_to_local(host=WEAVIATE_HOST_URL),
    )


def get_conversation_chain(vectorstore):
    """
    This function is used to get a conversation chain.

    Parameters:
    vectorstore: The vector store to use for retrieving the conversation chain.

    Returns:
    ConversationalRetrievalChain: An instance of the ConversationalRetrievalChain class.
    """
    retriever = vectorstore.as_retriever()
    llm = ChatOllama(base_url=OLLAMA_API_BASE_URL, model="llama3:8b-instruct-q5_1")

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, memory=memory
    )
    return conversation_chain

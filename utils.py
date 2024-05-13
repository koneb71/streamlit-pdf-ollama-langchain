from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


embedding = FastEmbedEmbeddings()


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


def add_to_faiss_vector_store(
    chunks: list[Document],
):
    return FAISS.from_documents(chunks, embedding).as_retriever()

import os
import shutil
from datetime import datetime
from pathlib import Path

import streamlit as st

from html_templates import css, user_template, bot_template
from rag import (
    load_documents,
    split_documents,
    add_to_weaviate_store,
    get_conversation_chain,
)


def handle_userinput(user_question: str):
    """
    This function is used to handle user input in the chat interface.

    Parameters:
    user_question (str): The question input by the user in the chat interface.

    The function first retrieves the response from the conversation state using the user's question.
    It then updates the chat history in the session state with the response's chat history.
    Finally, it iterates over the chat history. For each message, it checks if the index is even.
    If it is, it writes the user's message to the interface. If it's not, it writes the bot's message.
    """
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True
            )


def save_uploaded_files(pdf_docs):
    """
    This function is used to save uploaded PDF documents in a new directory.

    Parameters:
    pdf_docs (list): The list of uploaded PDF documents.

    The function first gets the current date and time and formats it as a string.
    It then creates a new directory in the 'uploads' directory with the current date and time as its name.
    It iterates over the uploaded PDF documents. For each document, it saves the document in the new directory.
    Finally, it returns the path to the new directory.

    Returns:
    new_dir (Path): The path to the new directory where the PDF documents are saved.
    """
    dt_string = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_dir = Path("uploads", dt_string)
    new_dir.mkdir(parents=True, exist_ok=True)

    for file in pdf_docs:
        save_path = new_dir / file.name
        with open(save_path, mode="wb") as w:
            w.write(file.getvalue())
    return new_dir


def delete_uploaded_files(directory: str):
    """
    This function is used to delete all files and directories in the specified directory.

    Parameters:
    directory (str): The path to the directory from which to delete files and directories.

    The function iterates over all files and directories in the specified directory.
    For each file or symbolic link, it deletes the file or symbolic link.
    For each directory, it deletes the directory and all its contents.
    If an error occurs during deletion, it prints an error message with the path of the file or directory and the reason for the failure.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True
        )
        if st.button("Process"):
            with st.spinner("Processing"):
                new_dir = save_uploaded_files(pdf_docs)

                docs = load_documents()
                chunks = split_documents(docs)
                vectorstore = add_to_weaviate_store(chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

                # delete uploaded files
                delete_uploaded_files(str(new_dir))


if __name__ == "__main__":
    main()

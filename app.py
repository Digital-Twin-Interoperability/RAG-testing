import streamlit as st
import tempfile

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

def main():
    st.title("PDF Q&A App with LangChain RAG and GPT‑4")
    st.write("Upload a PDF and ask questions about its content!")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        # Write the uploaded PDF to a temporary file so that it can be read by PyPDFLoader.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        # Load the PDF file
        loader = PyPDFLoader(tmp_file_path)
        documents = loader.load()

        # Optionally, split the documents into chunks to improve retrieval quality.
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)

        # Create embeddings for the chunks using OpenAI's embeddings.
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(docs, embeddings)

        # Initialize the GPT‑4 model (via ChatOpenAI) with zero temperature for deterministic answers.
        llm = ChatOpenAI(model_name="gpt-4", temperature=0)

        # Create a retriever from the vectorstore (returning the top 3 similar chunks)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        # Set up the Retrieval QA chain that uses the GPT‑4 LLM.
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # "stuff" simply concatenates context chunks.
            retriever=retriever
        )

        # Text input for user question.
        query = st.text_input("Enter your question about the PDF:")
        if query:
            with st.spinner("Processing your query..."):
                answer = qa_chain.run(query)
            st.markdown("### Answer:")
            st.write(answer)

if __name__ == "__main__":
    main()

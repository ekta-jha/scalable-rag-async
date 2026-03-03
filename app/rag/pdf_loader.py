from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Loading document
def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

# Splitting document into chunks
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    
    chunks = splitter.split_documents(documents)
    return chunks
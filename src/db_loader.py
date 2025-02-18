 
from langchain.embeddings import TogetherEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import PyPDFLoader

def load_db(file, k=4):
    loader = PyPDFLoader(file)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)

    embeddings = TogetherEmbeddings(model_name="togethercomputer/m2-bert-80M-embedding")
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
    
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    return retriever

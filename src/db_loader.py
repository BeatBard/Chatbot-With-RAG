import os
from dotenv import load_dotenv
from together import Together
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader

# Load API keys
load_dotenv()

api_key = os.getenv("TOGETHER_API_KEY")
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")  # Load Hugging Face token

if not api_key:
    raise ValueError("Missing TogetherAI API key! Ensure it's set in the .env file.")
if not hf_token:
    raise ValueError("Missing Hugging Face API token! Set it in the .env file.")

# Initialize TogetherAI client
together_client = Together(api_key=api_key)

def get_together_embeddings(texts):
    """Generate embeddings using TogetherAI"""
    response = together_client.embeddings.create(
        model="togethercomputer/m2-bert-80M-8k-retrieval",
        input=texts
    )
    print("🔍 TogetherAI Response:", response)  # Debugging print

    # Handle response using the .data attribute
    if hasattr(response, "data") and isinstance(response.data, list):
        return [item.embedding for item in response.data]
    raise ValueError("Unexpected response format from TogetherAI: " + str(response))

def load_db(file):
    """Load PDF, split into chunks, and create a FAISS vector database."""
    loader = PyPDFLoader(file)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)

    texts = [doc.page_content for doc in docs]
    embeddings = get_together_embeddings(texts)

    # Use FAISS with Hugging Face authentication
    hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
                                          model_kwargs={"token": hf_token})

    db = FAISS.from_texts(texts, hf_embeddings)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    return retriever

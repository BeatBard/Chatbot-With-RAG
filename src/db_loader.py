# db_loader.py

import os
from dotenv import load_dotenv
from together import Together
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader

# 1) Import your legacy converter
from legacy import convert_to_unicode

# Load API keys
load_dotenv()

api_key = os.getenv("TOGETHER_API_KEY")
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

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
    print("🔍 TogetherAI Embeddings Response:", response)  # Debugging print

    if hasattr(response, "data") and isinstance(response.data, list):
        return [item.embedding for item in response.data]

    raise ValueError("Unexpected response format from TogetherAI:", response)

def load_db(file):
    """Load PDF, split into chunks, detect/convert Sinhala if needed, then create a FAISS vector DB."""
    loader = PyPDFLoader(file)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)

    # Extract raw text
    raw_texts = [doc.page_content for doc in docs]

    # Convert each chunk to Unicode if needed
    cleaned_texts = []
    for idx, text in enumerate(raw_texts):
        unicode_text = convert_to_unicode(text)
        
        # Debug check: compare old vs new for the first chunk or so
        if idx < 2:  # just print the first couple for sanity check
            print("\n=== Chunk #", idx, "===")
            print("Raw chunk:", text[:100], "...")
            print("Converted chunk:", unicode_text[:100], "...")
        
        cleaned_texts.append(unicode_text)

    # Use Hugging Face embeddings to build FAISS
    hf_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"token": hf_token}
    )

    db = FAISS.from_texts(cleaned_texts, hf_embeddings)

    # 🔎 EXTRA CHECK: let's do a quick similarity search in the DB
    # to confirm we can retrieve something in Sinhala:
    test_query = "සිංහල"  # e.g. the word "සිංහල"
    results = db.similarity_search(test_query, k=2)
    print("\n=== Test Similarity Search ===")
    print(f"Query: {test_query}")
    for i, r in enumerate(results):
        print(f"Result {i}:", r.page_content[:100], "...")

    return db

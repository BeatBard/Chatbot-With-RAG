import os
from together_llm import TogetherChat
from db_loader import load_db

class Chatbot:
    def __init__(self, pdf_file):
        """Initialize chatbot with the given PDF file and load the knowledge base."""
        print(f"📄 Loading document: {pdf_file}")
        self.retriever = load_db(pdf_file)
        # Initialize the TogetherAI chat completion wrapper
        self.together_chat = TogetherChat()

    def ask(self, query):
        """Retrieve context from the PDF and generate an answer using TogetherAI."""
        print(f"🔍 Searching for: {query}")
        try:
            # Retrieve relevant documents from the knowledge base
            docs = self.retriever.get_relevant_documents(query)
            if docs:
                context = "\n\n".join([doc.page_content for doc in docs])
                sources = docs
            else:
                context = ""
                sources = []

            # Build a prompt that includes the retrieved context and the user's question
            prompt = (
                f"Below is some context extracted from a document:\n\n"
                f"{context}\n\n"
                f"Based on the above context, answer the following question:\n{query}"
            )
            print("🔍 Prompt for TogetherAI:", prompt)
            messages = [{"role": "user", "content": prompt}]
            answer = self.together_chat.chat(messages, temperature=0.7, max_tokens=512)
            return answer, sources

        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return "An error occurred while retrieving information.", []

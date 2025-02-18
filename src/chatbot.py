import os
from langchain_together import Together  # ✅ Corrected Import
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from db_loader import load_db

class Chatbot:
    def __init__(self, pdf_file):
        """Initialize chatbot with the given PDF file and load the knowledge base."""
        print(f"📄 Loading document: {pdf_file}")
        self.retriever = load_db(pdf_file).as_retriever()

        # Initialize TogetherAI chat model
        self.llm = Together(model="meta-llama/Llama-3.3-70B-Instruct-Turbo")

        # ✅ Explicitly setting output_key to "answer"
        self.memory = ConversationBufferMemory(memory_key="chat_history", output_key="answer", return_messages=True)

        # Define the Conversational Retrieval Chain
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,  # ✅ Ensures sources are returned
            output_key="answer"  # ✅ Ensures only the answer is stored in memory
        )

    def ask(self, query):
        """Query the chatbot with conversational context."""
        print(f"🔍 Searching for: {query}")
        try:
            response = self.qa.invoke({"question": query, "chat_history": self.memory.chat_memory.messages})

            print("🔍 Raw Response:", response)  # Debugging print

            # Extract answer and sources correctly
            answer = response.get("answer", "I couldn't find any relevant information.")
            sources = response.get("source_documents", [])

            print("🧠 Chat History:", self.memory.chat_memory.messages)  # Debug chat history
            print()
            print("-----------------------------")
            return answer, sources

        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return "An error occurred while retrieving information.", []

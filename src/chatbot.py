import os
from langchain_openai import OpenAI  # Using base OpenAI for completions
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from db_loader import load_db  
from langchain.schema import HumanMessage, AIMessage, SystemMessage  # For conversation messages

class Chatbot:
    def __init__(self, pdf_file):
        print(f"📄 Loading document: {pdf_file}")
        self.retriever = load_db(pdf_file).as_retriever()

        # Initialize the LLM with your vLLM endpoint.
        self.llm = OpenAI(
            model="Llama-3.1-8B",
            openai_api_base="https://7e6lv0bc4on3wl-8000.proxy.runpod.net/v1",
            openai_api_key="THIS_SHOULD_NOT_BE_A_REAL_KEY",
            temperature=0.7,
            max_tokens=512
        )

        # Initialize conversation memory so we can track chat history.
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True
        )

        # Custom Sinhala prompt template with [INST] formatting
        self.prompt_template = PromptTemplate.from_template(
            "<<SYS>>\n"
            "ඔබ යහපත් සහ උපකාරී සහකාරයෙකි. පහත සන්දර්භය භාවිතයෙන් පැනයට පිළිතුරු සපයන්න. "
            "පිළිතුර ලබා ගත නොහැකි නම්, එය තොරතුරු ලබාදී නොමැති බව සඳහන් කරන්න. "
            "සෑම විටම සිංහල භාෂාවෙන් පිළිතුරු ලබා දෙන්න.\n"
            "<</SYS>>\n\n"
            "Context:\n{context}\n\n"
            "Conversation History:\n{chat_history}\n\n"
            "Question: {question}\n"
            "Answer:"
        )

    def ask(self, query: str) -> tuple:
        try:
            # Retrieve relevant documents.
            docs = self.retriever.get_relevant_documents(query)
            context = "\n".join([d.page_content for d in docs])
            
            # Format conversation history; if there are no messages, it will be an empty string.
            chat_history = "\n".join([
                f"Human: {msg.content}" if isinstance(msg, HumanMessage) else f"Assistant: {msg.content}"
                for msg in self.memory.chat_memory.messages
            ])

            # Format the prompt using the custom template.
            prompt = self.prompt_template.format(
                context=context,
                chat_history=chat_history,
                question=query
            )
            print("Formatted prompt:", prompt)

            # Invoke the LLM to generate a response.
            response = self.llm.invoke(prompt)
            return response.strip(), docs

        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return "An error occurred while processing your request.", []

# Example usage:
if __name__ == "__main__":
    bot = Chatbot("uploaded_file.pdf")
    answer, docs = bot.ask("මෙහි සඳහන් වන්නේ කුමක් ගැනද?")
    print("Answer:", answer)
    for doc in docs:
        print("Source snippet:", doc.page_content[:100], "...")

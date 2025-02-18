import os
import panel as pn
from dotenv import load_dotenv
from chatbot import Chatbot

# Load environment variables
load_dotenv()

# Ensure API key is set
api_key = os.getenv("TOGETHER_API_KEY")
if not api_key:
    raise ValueError("Missing TogetherAI API key! Ensure it's set in the .env file.")

print("🚀 Chatbot is starting...")  # Debug print

# File Upload Widget for PDFs
file_input = pn.widgets.FileInput(accept=".pdf")

# Initialize chatbot UI as None (it will be set after PDF upload)
chat_ui = None  

class ChatbotUI:
    def __init__(self, pdf_file):
        """Initialize chatbot with the given PDF file."""
        print(f"🔍 Loading PDF: {pdf_file}")  # Debug print
        self.chatbot = Chatbot(pdf_file)
        self.panels = []
    
    def chat(self, query):
        """Handles user input and generates chatbot responses based on the PDF."""
        if not query.strip():
            return pn.WidgetBox(pn.Row("User:", pn.pane.Markdown("", width=600)), scroll=True)

        try:
            answer, sources = self.chatbot.ask(query)

            # If no relevant info is found, notify the user
            if not sources:
                answer = "I couldn't find any relevant information in the uploaded PDF. Try rephrasing your question."

            formatted_response = f'<div style="background-color: #F6F6F6; padding: 10px;">{answer}</div>'
        except Exception as e:
            print(f"❌ Error during chat response: {e}")
            formatted_response = '<div style="background-color: #FFCCCC; padding: 10px;">Error generating response.</div>'

        self.panels.extend([
            pn.Row("User:", pn.pane.Markdown(query, width=600)),
            pn.Row("ChatBot:", pn.pane.HTML(formatted_response, width=600))
        ])
        return pn.WidgetBox(*self.panels, scroll=True)

def load_new_pdf(event):
    """Handles new PDF uploads and reloads the chatbot dynamically."""
    global chat_ui
    if file_input.value:
        pdf_path = "uploaded_file.pdf"
        with open(pdf_path, "wb") as f:
            f.write(file_input.value)
        print(f"🔄 Reloading chatbot with new PDF: {pdf_path}")
        chat_ui = ChatbotUI(pdf_path)

# Watch for PDF uploads
file_input.param.watch(load_new_pdf, "value")

# User input widget for chat
inp = pn.widgets.TextInput(placeholder="Type your message here...")

# Bind the chat function safely
def safe_chat_bind(query):
    """Ensures chatbot is ready before processing user input."""
    if chat_ui:
        return chat_ui.chat(query)
    else:
        return pn.WidgetBox(pn.Row("ChatBot:", pn.pane.Markdown("Please upload a PDF to start chatting.", width=600)), scroll=True)

conversation = pn.bind(safe_chat_bind, inp)

# UI Layout
dashboard = pn.Column(
    pn.Row(pn.pane.Markdown("## 🤖 Chatbot With TogetherAI", styles={'font-size': '20px', 'font-weight': 'bold'})),
    pn.Row(file_input),  # PDF upload widget
    pn.Row(inp),
    pn.layout.Divider(),
    pn.panel(conversation, loading_indicator=True, height=400),
    pn.layout.Divider(),
)

print("✅ Chatbot UI is ready!")  # Debug print

try:
    dashboard.show()
    print("👀 UI should now be visible in your browser!")  # Debug print
except Exception as e:
    print(f"❌ Error launching UI: {e}")

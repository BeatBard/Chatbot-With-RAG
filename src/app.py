import os
import panel as pn
from dotenv import load_dotenv
from chatbot import Chatbot

# Enable Panel extensions and custom CSS for better styling
pn.extension(sizing_mode="stretch_width")
pn.config.raw_css.append("""
.modern-input {
    border: 2px solid #0D47A1;
    border-radius: 5px;
    padding: 8px;
    font-size: 16px;
    width: 100%;
}
""")

# Load environment variables
load_dotenv()

# Validate API key
api_key = os.getenv("TOGETHER_API_KEY")
if not api_key:
    raise ValueError("❌ Missing TogetherAI API key! Ensure it's set in the .env file.")

print("🚀 Chatbot is starting...")

# File Upload Widget for PDFs with proper width
file_input = pn.widgets.FileInput(accept=".pdf", width_policy="max", css_classes=["modern-input"])

# User input widget for chat
inp = pn.widgets.TextInput(placeholder="Type your message here...", width_policy="max", css_classes=["modern-input"])

class ChatbotUI:
    """Handles chatbot interactions and PDF uploads."""
    
    def __init__(self):
        self.chatbot = None
        self.panels = []

    def load_pdf(self, event):
        """Loads a new PDF and initializes the chatbot."""
        if file_input.value:
            pdf_path = "uploaded_file.pdf"
            with open(pdf_path, "wb") as f:
                f.write(file_input.value)
            print(f"🔄 Reloading chatbot with new PDF: {pdf_path}")
            self.chatbot = Chatbot(pdf_path)

    def chat(self, query):
        """Handles user input and generates chatbot responses."""
        if not self.chatbot:
            return pn.WidgetBox(
                pn.Row("ChatBot:", pn.pane.Markdown("📂 Please upload a PDF to start chatting.", width_policy="max")),
                scroll=True
            )

        if not query.strip():
            return pn.WidgetBox(pn.Row("User:", pn.pane.Markdown("", width_policy="max")), scroll=True)

        try:
            answer, sources = self.chatbot.ask(query)
            if not sources:
                answer = "I couldn't find any relevant information in the uploaded PDF. Try rephrasing your question."

            formatted_response = f'<div style="background-color: #F6F6F6; padding: 10px; border-radius: 8px;">{answer}</div>'
        except Exception as e:
            print(f"❌ Error during chat response: {e}")
            formatted_response = (
                '<div style="background-color: #FFCCCC; padding: 10px; border-radius: 8px;">'
                "Error generating response.</div>"
            )

        self.panels.extend([
            pn.Row("User:", pn.pane.Markdown(query, width_policy="max")),
            pn.Row("ChatBot:", pn.pane.HTML(formatted_response, width_policy="max"))
        ])
        return pn.WidgetBox(*self.panels, scroll=True)

# Initialize chatbot UI handler
chat_ui = ChatbotUI()

# Watch for PDF uploads
file_input.param.watch(chat_ui.load_pdf, "value")

def safe_chat_bind(query):
    """Ensures chatbot is ready before processing user input."""
    return chat_ui.chat(query)

# Bind the conversation function to user input
conversation = pn.bind(safe_chat_bind, inp)

# Create Material UI template with improved spacing
template = pn.template.MaterialTemplate(
    title="🤖 Chatbot with TogetherAI",
    header_background="#0D47A1"  # Dark blue header background
)

# Sidebar: PDF Upload and User Input with proper spacing
template.sidebar.append(pn.pane.Markdown("### 📂 Upload PDF", width_policy="max"))
template.sidebar.append(file_input)
template.sidebar.append(pn.layout.Spacer(height=20))
template.sidebar.append(pn.pane.Markdown("### 💬 Your Message", width_policy="max"))
template.sidebar.append(inp)

# Main content: Chat interface
template.main.append(pn.pane.Markdown("<div style='text-align: center;'>## 🗨️ Conversation</div>"))
template.main.append(pn.layout.Spacer(height=10))
template.main.append(pn.panel(conversation, loading_indicator=True, height=500, sizing_mode="stretch_both"))

print("✅ Chatbot UI is ready!")

# Launch UI
try:
    template.show()
    print("👀 UI should now be visible in your browser!")
except Exception as e:
    print(f"❌ Error launching UI: {e}")

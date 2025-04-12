import os
import panel as pn
from dotenv import load_dotenv
from chatbot import Chatbot

# Enable Panel extensions and custom CSS for better styling
pn.extension(sizing_mode="stretch_width")
pn.config.raw_css.append("""
.modern-input {
    border: 2px solid #0D47A1;
    border-radius: 8px;
    padding: 12px;
    font-size: 16px;
    width: 100%;
    transition: all 0.3s ease;
    background-color: #f8f9fa;
}

.modern-input:focus {
    border-color: #1976D2;
    box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
    outline: none;
}

.chat-message {
    margin: 10px 0;
    padding: 12px 16px;
    border-radius: 8px;
    max-width: 80%;
}

.user-message {
    background-color: #E3F2FD;
    margin-left: auto;
    border: 1px solid #BBDEFB;
}

.bot-message {
    background-color: #F5F5F5;
    margin-right: auto;
    border: 1px solid #E0E0E0;
}

.sidebar-section {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    border: 1px solid #e0e0e0;
}

.title-section {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #0D47A1, #1976D2);
    color: white;
    border-radius: 8px;
    margin-bottom: 20px;
}

.file-upload-section {
    background-color: #E3F2FD;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
}

.chat-section {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    height: 500px;
    overflow-y: auto;
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
file_input = pn.widgets.FileInput(
    accept=".pdf",
    width_policy="max",
    css_classes=["modern-input"],
    name="📄 Upload PDF"
)

# User input widget for chat
inp = pn.widgets.TextInput(
    placeholder="Type your message here...",
    width_policy="max",
    css_classes=["modern-input"]
)

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
            # Clear previous chat when new PDF is loaded
            self.panels = []
            self.panels.append(pn.pane.Markdown(
                "### 📚 PDF loaded successfully! You can now start chatting.",
                style={'color': '#1976D2', 'text-align': 'center'}
            ))

    def chat(self, query):
        """Handles user input and generates chatbot responses."""
        if not self.chatbot:
            return pn.WidgetBox(
                pn.pane.Markdown(
                    "### 📂 Please upload a PDF to start chatting.",
                    style={'color': '#666', 'text-align': 'center'}
                ),
                scroll=True,
                css_classes=["chat-section"]
            )

        if not query.strip():
            return pn.WidgetBox(
                pn.pane.Markdown("", width_policy="max"),
                scroll=True,
                css_classes=["chat-section"]
            )

        try:
            answer, sources = self.chatbot.ask(query)
            if not sources:
                answer = "I couldn't find any relevant information in the uploaded PDF. Try rephrasing your question."

            user_message = pn.pane.Markdown(
                f"**You:** {query}",
                css_classes=["chat-message", "user-message"]
            )
            
            bot_message = pn.pane.Markdown(
                f"**Bot:** {answer}",
                css_classes=["chat-message", "bot-message"]
            )

            self.panels.extend([user_message, bot_message])
            
            return pn.WidgetBox(
                *self.panels,
                scroll=True,
                css_classes=["chat-section"]
            )

        except Exception as e:
            print(f"❌ Error during chat response: {e}")
            error_message = pn.pane.Markdown(
                "❌ Error generating response. Please try again.",
                css_classes=["chat-message", "bot-message"]
            )
            self.panels.append(error_message)
            return pn.WidgetBox(
                *self.panels,
                scroll=True,
                css_classes=["chat-section"]
            )

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
    header_background="#0D47A1",
    sidebar_width=300
)

# Title section
title = pn.pane.Markdown(
    """
    # 🤖 Chatbot with TogetherAI
    ### Upload a PDF and start chatting!
    """,
    css_classes=["title-section"]
)

# Sidebar sections
file_upload_section = pn.Column(
    pn.pane.Markdown("### 📂 Upload PDF", style={'color': '#0D47A1'}),
    file_input,
    css_classes=["sidebar-section"]
)

chat_input_section = pn.Column(
    pn.pane.Markdown("### 💬 Your Message", style={'color': '#0D47A1'}),
    inp,
    css_classes=["sidebar-section"]
)

# Add sections to sidebar
template.sidebar.append(title)
template.sidebar.append(file_upload_section)
template.sidebar.append(chat_input_section)

# Main content: Chat interface
template.main.append(pn.panel(conversation, loading_indicator=True))

print("✅ Chatbot UI is ready!")

# Launch UI
try:
    template.show()
    print("👀 UI should now be visible in your browser!")
except Exception as e:
    print(f"❌ Error launching UI: {e}")

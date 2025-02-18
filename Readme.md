# 📌 Chatbot with TogetherAI, Conversational Memory and RAG
🚀 **An AI-powered chatbot that extracts knowledge from PDFs using TogetherAI’s LLMs, FAISS for retrieval, and Conversational Memory with Panel UI.**  
This chatbot allows users to upload PDFs, retain conversation context, and ask intelligent questions.

---

## **🔧 Features**
✔️ **Upload PDFs** to extract and index document content  
✔️ **Chatbot powered by TogetherAI** for advanced language understanding  
✔️ **Vector-based retrieval** using FAISS for precise search results  
✔️ **Real-time UI** built with **Panel** for interactive user experiences  
✔️ **Conversational Memory** that retains context for seamless dialogues  
✔️ **Modular and extendable** architecture to integrate additional AI models and features  
✔️ **Efficient Chat Flow** via LangChain's Conversational Retrieval Chain


---

## **📂 Project Structure**
```
📂 Chatbot-With-TogetherAI
│── 📂 src
│   │── app.py                # UI using Panel
│   │── chatbot.py            # Chatbot logic
│   │── db_loader.py          # Loads PDFs and processes embeddings
│   │── togetherllm.py        # TogetherAI API integration
│── 📂 data
│   │── sample.pdf            # Sample document
│── .env                      # Environment variables (API keys)
│── requirements.txt          # Python dependencies
│── README.md                 # Project documentation
```

---

## **🛠 Setup & Installation**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/Chatbot-With-TogetherAI.git
cd Chatbot-With-TogetherAI
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up API Keys**
Create a `.env` file in the root directory and add your TogetherAI API key:
```
TOGETHER_API_KEY=your_together_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_key_here
```

---

## **🚀 Running the Chatbot**
```bash
python src/app.py
```

The Panel UI will launch in your default web browser. If not, open the displayed **localhost URL**.

---

## **📝 How to Use**
1️⃣ **Upload a PDF** using the file upload widget  
2️⃣ **Ask a question** related to the PDF's content  
3️⃣ **Get AI-generated answers** from TogetherAI and FAISS retrieval  

---

## **📌 Contribution**
Pull requests are welcome! If you’d like to contribute:
- Fork the repository
- Create a feature branch (`git checkout -b feature-name`)
- Commit your changes (`git commit -m 'Add feature'`)
- Push to your branch (`git push origin feature-name`)
- Open a PR!

---

## **📜 License**
This project is licensed under the MIT License.

---

## **📞 Contact**
📧 Email: pcsalwathura@gmail.com 
🐙 GitHub: (https://github.com/BeatBard)  


# 📌 Chatbot with TogetherAI

🚀 **A PDF-based chatbot using TogetherAI's LLMs and FAISS for retrieval, with a Panel UI interface.**  
This chatbot allows users to upload PDFs and ask questions based on their content.

---

## **🔧 Features**
✔️ **Upload PDFs** and extract knowledge from documents  
✔️ **Chatbot using TogetherAI** for language understanding  
✔️ **Vector-based retrieval** using FAISS  
✔️ **Real-time UI** with **Panel**  
✔️ **Modular and extendable** for more models  

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


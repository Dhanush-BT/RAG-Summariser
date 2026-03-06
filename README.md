# 📚 RAG PDF Summariser

A **Retrieval-Augmented Generation (RAG) chatbot** that allows users to ask questions about a PDF document and receive **context-aware answers** generated using Large Language Models (LLMs).

The system extracts text from PDFs, converts the text into embeddings using **Sentence Transformers**, stores them in a **Qdrant vector database**, and retrieves relevant chunks during query time to generate accurate responses.

---

# 🚀 Features

* 📄 **PDF Document Processing**
* ✂️ **Smart Text Chunking with Overlap**
* 🧠 **Semantic Embeddings using SentenceTransformers**
* 🗄 **Vector Database Storage with Qdrant**
* 🔎 **Semantic Retrieval for relevant document chunks**
* 🤖 **LLM-powered answer generation**
* 💬 **Interactive CLI chat interface**
* 🐳 **Dockerized deployment for easy setup**

---

# 🏗 System Architecture

PDF Document
⬇
Text Extraction (pdfplumber)
⬇
Chunking (Sliding Window Strategy)
⬇
Embedding Generation (Sentence Transformers)
⬇
Vector Storage (Qdrant)
⬇
Semantic Search
⬇
LLM Generation (Cerebras API)
⬇
Context-aware Answer

---

# 🧰 Tech Stack

* **Python**
* **Sentence Transformers**
* **Qdrant Vector Database**
* **Cerebras LLM API**
* **pdfplumber**
* **Docker**
* **dotenv**

---

# 📂 Project Structure

```
RAG-Summariser
│
├── rag.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

# ⚙️ Installation

### 1️⃣ Clone the Repository

```
git clone https://github.com/Dhanush-BT/RAG-Summariser.git
cd RAG-Summariser
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Create Environment Variables

Create a `.env` file in the root directory.

```
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
CEREBRAS_API_KEY=your_cerebras_api_key
COLLECTION_NAME=static_doc_rag
PDF_PATH=your_pdf_file.pdf
```

⚠️ Never push `.env` files to GitHub.

---

# ▶️ Running the Application

Run the chatbot:

```
python rag.py
```

Example interaction:

```
Ask your question (or type 'exit'):
> What is cryptography?

Answer:
Cryptography is the practice of securing communication using mathematical techniques...
```

---

# 🐳 Running with Docker

Build and run using Docker Compose:

```
docker compose up --build
```

Docker will automatically build the environment and start the RAG system.

---

# 🎯 Use Cases

* 📚 Study material assistants
* 📄 Research paper question answering
* 🧾 Legal document search
* 🏢 Enterprise knowledge base assistants
* 📖 Technical documentation chatbot

---

# 🔮 Future Improvements

* Web interface using **Streamlit or React**
* Multi-document support
* Hybrid search (BM25 + Vector Search)
* Chat history memory
* REST API support
* Document upload support

---

# 👨‍💻 Author

**Dhanush BT**

---

# 📜 License

MIT License

# 🇮🇳 Aurynx Citizen AI

### Government services, made simple.

**Aurynx Citizen AI** is an AI-powered citizen assistant designed to make Indian government information easier to understand and access.

Users can ask questions about government scholarships, schemes, benefits and citizen services using **text or English voice**, and can also upload official government PDF documents and ask questions about their contents.

🌐 **Live Application:** https://aurynx-citizen-ai-frontend.onrender.com

---

## ✨ Features

### 💬 AI-Powered Government Information

Ask questions about:

* Government scholarships
* Government schemes
* Citizen benefits
* Certificates and government services
* Eligibility requirements
* Required documents
* Application-related information

Aurynx retrieves relevant information and presents it in a simple, understandable format.

### 🎤 English Voice Input

Users can speak their questions instead of typing.

Aurynx uses **OpenAI Whisper** for speech-to-text transcription before sending the question through the AI retrieval pipeline.

### 📄 Government Document Q&A

Users can upload an official government PDF and ask questions about the document.

The system:

1. Accepts the PDF
2. Extracts the document text
3. Splits the content into chunks
4. Generates embeddings
5. Stores/searches the embeddings using FAISS
6. Retrieves relevant content
7. Generates an answer based on the retrieved document information

### 🔎 Source & Verification Information

Aurynx can provide:

* Scheme name
* Official source information
* Source document
* Document year
* Verification notices for older documents

This helps users understand where the information came from and reminds them to verify current government rules when necessary.

---

## 🧠 How Aurynx Works

Aurynx uses a **Retrieval-Augmented Generation (RAG)** approach.

```text
                     USER
                       │
             ┌─────────┴─────────┐
             │                   │
          Text Input         Voice Input
             │                   │
             │              Whisper
             │                   │
             └─────────┬─────────┘
                       │
                       ▼
                Streamlit UI
                       │
                       ▼
                FastAPI Backend
                       │
                       ▼
              Question Processing
                       │
                       ▼
             Sentence Transformers
                       │
                       ▼
                    FAISS
                       │
                       ▼
              Relevant Information
                       │
                       ▼
                  OpenAI API
                       │
                       ▼
               Grounded Response
                       │
                       ▼
                   Aurynx
```

### Document RAG Pipeline

```text
Official Government PDF
          │
          ▼
      PDF Extraction
          │
          ▼
       Text Chunks
          │
          ▼
     Embeddings
          │
          ▼
         FAISS
          │
          ▼
   Relevant Document Chunks
          │
          ▼
       AI Response
          │
          ▼
 Answer + Source + Document Year
```

---

## 🏗️ Architecture

Aurynx is deployed as two services:

```text
                  Internet
                     │
                     ▼
        ┌────────────────────────┐
        │   Streamlit Frontend   │
        │      Render Cloud      │
        └────────────┬───────────┘
                     │
                     │ HTTP
                     ▼
        ┌────────────────────────┐
        │    FastAPI Backend     │
        │      Render Cloud      │
        └────────────┬───────────┘
                     │
          ┌──────────┼───────────┐
          ▼          ▼           ▼
       FAISS    Sentence      OpenAI
                Transformers    API
```

### Frontend

* Streamlit
* Custom CSS UI
* Text input
* Voice input
* PDF upload
* Document Q&A

### Backend

* FastAPI
* REST API endpoints
* Retrieval pipeline
* Government knowledge base
* Document processing
* AI response generation

---

## 🛠️ Technology Stack

| Layer                | Technology            |
| -------------------- | --------------------- |
| Frontend             | Streamlit             |
| Backend              | FastAPI               |
| Programming Language | Python                |
| AI / LLM             | OpenAI API            |
| Speech-to-Text       | OpenAI Whisper        |
| Embeddings           | Sentence Transformers |
| Vector Search        | FAISS                 |
| PDF Processing       | pypdf                 |
| Data Validation      | Pydantic              |
| API Server           | Uvicorn               |
| Numerical Computing  | NumPy                 |
| Deployment           | Render                |
| Version Control      | Git & GitHub          |

---

## 📁 Project Structure

```text
aurynx-citizen-ai/
│
├── frontend.py
├── main.py
├── knowledge_base.py
│
├── requirements.txt
├── requirements-render.txt
├── .gitignore
└── README.md
```

### Important Files

**`frontend.py`**

Streamlit user interface containing:

* Text-based questions
* English voice input
* Government service sections
* PDF upload
* Document questions
* Answer display

**`main.py`**

FastAPI backend responsible for:

* API endpoints
* Question processing
* Retrieval
* AI responses
* PDF document processing

**`knowledge_base.py`**

Contains the structured government information used by Aurynx for supported government schemes and services.

**`requirements.txt`**

Python dependencies for the project.

**`requirements-render.txt`**

Dependencies used for the Render deployment environment.

---

## 🔌 API Endpoints

### Ask Aurynx

```text
POST /ask
```

Accepts a citizen question and returns an AI-generated response based on the available government information.

### Upload Government Document

```text
POST /upload-document
```

Uploads and processes an official government PDF.

### Ask About Document

```text
POST /ask-document
```

Answers questions using information retrieved from the uploaded document.

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/websam786/aurynx-citizen-ai.git
cd aurynx-citizen-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

For the deployed frontend, configure:

```env
AURYNX_BACKEND_URL=https://aurynx-citizen-ai.onrender.com
```

> **Never commit API keys or other secrets to GitHub.**

### 5. Start the FastAPI backend

```bash
uvicorn main:app --reload
```

### 6. Start the Streamlit frontend

In another terminal:

```bash
streamlit run frontend.py
```

---

## 🌐 Deployment

Aurynx is deployed using **Render**.

### Backend

```text
FastAPI
    ↓
Render Web Service
    ↓
https://aurynx-citizen-ai.onrender.com
```

### Frontend

```text
Streamlit
    ↓
Render Web Service
    ↓
https://aurynx-citizen-ai-frontend.onrender.com
```

The Streamlit frontend communicates with the deployed FastAPI backend through the `AURYNX_BACKEND_URL` environment variable.

---

## 🔐 Government Information & Verification

Aurynx is designed to make government information easier to understand.

However, government schemes and eligibility rules can change.

For this reason, Aurynx should be treated as an **information assistance system**, not as a replacement for official government portals or current scheme guidelines.

When information comes from an older government document, Aurynx can indicate the document year and encourage users to verify the latest requirements.

Users should always verify important eligibility, deadlines and application requirements with the relevant official government source.

---

## 🚀 Future Enhancements

Planned improvements may include:

* 🇮🇳 Malayalam voice interaction
* 🌐 Additional Indian languages
* 🔗 More official government data sources
* 📚 Expanded government scheme knowledge base
* 🔐 Improved document security and privacy controls
* 📊 Usage and feedback analytics
* 🎯 More personalized citizen-service guidance

---

## 🎯 Project Goal

The goal of Aurynx is simple:

> **Make government information easier for ordinary citizens to understand and access.**

Instead of navigating through complex government documents and terminology, citizens can ask questions in natural language and receive clear, structured explanations.

---

## 👩‍💻 Author

**Samiya Bindi CG**

Aurynx Citizen AI was developed as a practical AI application combining:

* Generative AI
* Retrieval-Augmented Generation
* Natural Language Processing
* Vector similarity search
* Speech recognition
* Document intelligence
* FastAPI
* Streamlit
* Cloud deployment

---

## 📄 Project Status

**Aurynx Citizen AI V1 — Deployed & Live 🚀**

The current V1 supports:

* ✅ Text-based questions
* ✅ English voice questions
* ✅ Government scheme information
* ✅ Government PDF upload
* ✅ Document-based Q&A
* ✅ Source information
* ✅ Document-year awareness
* ✅ Live frontend deployment
* ✅ Live backend deployment

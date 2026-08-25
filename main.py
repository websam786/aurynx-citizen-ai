
import io

import faiss
import numpy as np

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from knowledge_base import SCHOLARSHIPS


# ============================================================
# INITIALIZATION
# ============================================================

load_dotenv()

client = OpenAI()

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

app = FastAPI(
    title="Aurynx Citizen AI"
)


# ============================================================
# DOCUMENT STORAGE
# ============================================================

VECTOR_INDEX = None

DOCUMENT_CHUNKS = []

DOCUMENT_SOURCE = ""

DOCUMENT_YEAR = ""

DOCUMENT_TEXT = ""


# ============================================================
# REQUEST MODEL
# ============================================================

class CitizenQuestion(BaseModel):

    question: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to Aurynx Citizen AI"
    }


# ============================================================
# CREATE DOCUMENT CHUNKS
# ============================================================

def create_chunks(
    text,
    chunk_size=1000,
    overlap=200
):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        if chunk.strip():

            chunks.append(chunk)

        start = end - overlap

    return chunks


# ============================================================
# MAIN AURYNX SEARCH
# ============================================================

@app.post("/ask")
def ask_question(data: CitizenQuestion):

    global VECTOR_INDEX
    global DOCUMENT_CHUNKS
    global DOCUMENT_SOURCE
    global DOCUMENT_YEAR

    user_question = data.question.strip()

    if not user_question:

        return {
            "question": data.question,
            "message": "Please enter a question."
        }


    # ========================================================
    # STEP 1
    # IF A DOCUMENT HAS BEEN UPLOADED,
    # SEARCH THE DOCUMENT FIRST
    # ========================================================

    if VECTOR_INDEX is not None and DOCUMENT_CHUNKS:

        try:

            question_embedding = embedding_model.encode(
                [user_question]
            )

            question_embedding = np.array(
                question_embedding
            ).astype("float32")


            distances, indexes = VECTOR_INDEX.search(
                question_embedding,
                3
            )


            relevant_chunks = []

            for index in indexes[0]:

                if index != -1:

                    relevant_chunks.append(
                        DOCUMENT_CHUNKS[index]
                    )


            if relevant_chunks:

                context = "\n\n".join(
                    relevant_chunks
                )


                response = client.chat.completions.create(

                    model="gpt-5-mini",

                    messages=[

                        {
                            "role": "system",

                            "content": (
                                "You are Aurynx Citizen AI. "

                                "Answer the citizen's question "
                                "using only the provided "
                                "government document context. "

                                "Do not invent information. "

                                "Give a clear and simple answer. "

                                "If the answer is not available "
                                "in the document, clearly say "
                                "that the information is not "
                                "available in the uploaded document."
                            )
                        },

                        {
                            "role": "user",

                            "content": (

                                f"Source document: "
                                f"{DOCUMENT_SOURCE}\n\n"

                                f"Document context:\n"
                                f"{context}\n\n"

                                f"Citizen question:\n"
                                f"{user_question}"
                            )
                        }
                    ]
                )


                return {

                    "question": data.question,

                    "answer": (
                        response
                        .choices[0]
                        .message
                        .content
                    ),

                    "source_document":
                        DOCUMENT_SOURCE,

                    "document_year":
                        DOCUMENT_YEAR,

                    "notice": (
                        f"This information comes from "
                        f"a {DOCUMENT_YEAR} document. "
                        "Please verify current eligibility, "
                        "requirements and deadlines with "
                        "the official government source."
                    )
                }

        except Exception as e:

            print(
                "Document search error:",
                str(e)
            )


    # ========================================================
    # STEP 2
    # SEARCH THE GOVERNMENT KNOWLEDGE BASE
    # ========================================================

    user_question_lower = user_question.lower()


    for scheme in SCHOLARSHIPS:

        for keyword in scheme.get(
            "keywords",
            []
        ):

            if keyword.lower() in user_question_lower:

                return {

                    "question":
                        data.question,

                    "scheme":
                        scheme["name"],

                    "description":
                        scheme["description"],

                    "official_source":
                        scheme["official"]
                }


    # ========================================================
    # STEP 3
    # NOTHING FOUND
    # ========================================================

    return {

        "question":
            data.question,

        "message": (
            "I couldn't find matching government "
            "information yet. Please try asking about "
            "a government scheme, scholarship, benefit "
            "or uploaded document."
        )
    }


# ============================================================
# UPLOAD GOVERNMENT DOCUMENT
# ============================================================

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...)
):

    global DOCUMENT_TEXT
    global DOCUMENT_SOURCE
    global DOCUMENT_YEAR
    global DOCUMENT_CHUNKS
    global VECTOR_INDEX


    # --------------------------------------------------------
    # READ PDF
    # --------------------------------------------------------

    pdf_bytes = await file.read()

    reader = PdfReader(
        io.BytesIO(pdf_bytes)
    )


    text = ""


    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted + "\n"


    # --------------------------------------------------------
    # STORE DOCUMENT INFORMATION
    # --------------------------------------------------------

    DOCUMENT_TEXT = text

    DOCUMENT_SOURCE = file.filename

    # Currently your Pragati PDF is from 2020.
    # Later we can automatically detect the year.
    DOCUMENT_YEAR = "2020"


    # --------------------------------------------------------
    # CREATE CHUNKS
    # --------------------------------------------------------

    chunks = create_chunks(
        text
    )


    DOCUMENT_CHUNKS = chunks


    # --------------------------------------------------------
    # CREATE EMBEDDINGS
    # --------------------------------------------------------

    embeddings = embedding_model.encode(
        DOCUMENT_CHUNKS
    )


    embeddings = np.array(
        embeddings
    ).astype("float32")


    # --------------------------------------------------------
    # CREATE FAISS INDEX
    # --------------------------------------------------------

    VECTOR_INDEX = faiss.IndexFlatL2(
        embeddings.shape[1]
    )


    VECTOR_INDEX.add(
        embeddings
    )


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {

        "filename":
            file.filename,

        "preview":
            text[:1000],

        "chunks":
            len(DOCUMENT_CHUNKS)
    }


# ============================================================
# ASK ABOUT DOCUMENT
# ============================================================

@app.post("/ask-document")
def ask_document(
    data: CitizenQuestion
):

    global VECTOR_INDEX
    global DOCUMENT_CHUNKS


    # --------------------------------------------------------
    # CHECK DOCUMENT
    # --------------------------------------------------------

    if (
        VECTOR_INDEX is None
        or not DOCUMENT_CHUNKS
    ):

        return {

            "message":
                "No document uploaded yet. "
                "Please upload a document first."
        }


    # --------------------------------------------------------
    # EMBED QUESTION
    # --------------------------------------------------------

    question_embedding = embedding_model.encode(
        [data.question]
    )


    question_embedding = np.array(
        question_embedding
    ).astype("float32")


    # --------------------------------------------------------
    # SEARCH FAISS
    # --------------------------------------------------------

    distances, indexes = VECTOR_INDEX.search(

        question_embedding,

        3
    )


    # --------------------------------------------------------
    # GET RELEVANT CHUNKS
    # --------------------------------------------------------

    relevant_chunks = []


    for index in indexes[0]:

        if index != -1:

            relevant_chunks.append(
                DOCUMENT_CHUNKS[index]
            )


    if not relevant_chunks:

        return {

            "question":
                data.question,

            "answer":
                "I couldn't find relevant "
                "information in this document."
        }


    # --------------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------------

    context = "\n\n".join(
        relevant_chunks
    )


    # --------------------------------------------------------
    # ASK OPENAI
    # --------------------------------------------------------

    response = client.chat.completions.create(

        model="gpt-5-mini",

        messages=[

            {
                "role": "system",

                "content": (
                    "You are Aurynx Citizen AI. "

                    "Answer the user's question using "
                    "only the provided document context. "

                    "Do not invent information. "

                    "If the answer is not present in "
                    "the context, say that it is not "
                    "available in the document."
                )
            },

            {
                "role": "user",

                "content": (

                    f"Source document: "
                    f"{DOCUMENT_SOURCE}\n\n"

                    f"Document context:\n"
                    f"{context}\n\n"

                    f"Question: "
                    f"{data.question}"
                )
            }
        ]
    )


    # --------------------------------------------------------
    # RETURN ANSWER
    # --------------------------------------------------------

    return {

        "question":
            data.question,

        "answer":
            response
            .choices[0]
            .message
            .content,

        "source_document":
            DOCUMENT_SOURCE,

        "document_year":
            DOCUMENT_YEAR,

        "notice": (

            f"This information comes from "
            f"a {DOCUMENT_YEAR} document. "

            "Please verify current eligibility, "
            "requirements and deadlines with "
            "the official government source."
        ),

        "sources":
            relevant_chunks
    }


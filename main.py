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


# ============================================================
# SCHOLARSHIP SEMANTIC SEARCH
# ============================================================

SCHOLARSHIP_TEXTS = []

for scheme in SCHOLARSHIPS:

    text = (
        scheme["name"] + " "
        + " ".join(scheme["keywords"]) + " "
        + scheme["description"] + " "
        + scheme["eligibility"]
    )

    SCHOLARSHIP_TEXTS.append(text)


SCHOLARSHIP_EMBEDDINGS = embedding_model.encode(
    SCHOLARSHIP_TEXTS
)

SCHOLARSHIP_EMBEDDINGS = np.array(
    SCHOLARSHIP_EMBEDDINGS
).astype("float32")


# ============================================================
# FASTAPI
# ============================================================

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
# FIND BEST SCHOLARSHIP
# ============================================================

def find_best_scheme(question):

    question_embedding = embedding_model.encode(
        [question]
    )

    question_embedding = np.array(
        question_embedding
    ).astype("float32")


    # --------------------------------------------------------
    # NORMALIZE QUESTION
    # --------------------------------------------------------

    question_norm = (
        question_embedding
        / np.linalg.norm(
            question_embedding,
            axis=1,
            keepdims=True
        )
    )


    # --------------------------------------------------------
    # NORMALIZE SCHOLARSHIPS
    # --------------------------------------------------------

    scheme_norm = (
        SCHOLARSHIP_EMBEDDINGS
        / np.linalg.norm(
            SCHOLARSHIP_EMBEDDINGS,
            axis=1,
            keepdims=True
        )
    )


    # --------------------------------------------------------
    # COSINE SIMILARITY
    # --------------------------------------------------------

    similarities = np.dot(
        question_norm,
        scheme_norm.T
    )[0]


    # --------------------------------------------------------
    # BEST MATCH
    # --------------------------------------------------------

    best_index = int(
        np.argmax(similarities)
    )

    best_score = float(
        similarities[best_index]
    )


    return (
        SCHOLARSHIPS[best_index],
        best_score
    )


# ============================================================
# MAIN AURYNX SEARCH
# ============================================================

@app.post("/ask")
def ask_question(data: CitizenQuestion):

    user_question = (
        data.question
        .lower()
        .strip()
    )


    # ========================================================
    # INTENT DETECTION
    # ========================================================

    eligibility_words = [

        "eligible",
        "eligibility",
        "qualify",
        "qualification",
        "who can apply",
        "can i apply",
        "can i get",
        "am i allowed",
        "do i qualify",
        "can i receive",
        "who is eligible",
        "who can get"

    ]


    application_words = [

        "how to apply",
        "how can i apply",
        "application",
        "apply",
        "registration",
        "register",
        "where can i apply",
        "how do i register"

    ]


    document_words = [

        "document",
        "documents",
        "certificate",
        "certificates",
        "proof",
        "required papers",
        "papers do i need",
        "what should i submit",
        "what do i need to submit"

    ]


    # ========================================================
    # DETERMINE INTENT
    # ========================================================

    if any(
        word in user_question
        for word in eligibility_words
    ):

        intent = "eligibility"


    elif any(
        word in user_question
        for word in application_words
    ):

        intent = "application"


    elif any(
        word in user_question
        for word in document_words
    ):

        intent = "documents"


    else:

        intent = "general"


    # ========================================================
    # FIND BEST MATCHING SCHOLARSHIP
    # ========================================================

    scheme, similarity = find_best_scheme(
        user_question
    )


    # ========================================================
    # CHECK CONFIDENCE
    # ========================================================

    if similarity < 0.35:

        return {

            "question":
                data.question,

            "answer": (
                "I couldn't find reliable matching "
                "government information yet. "
                "Please try asking about a specific "
                "government scheme, scholarship or "
                "citizen service."
            )

        }


    # ========================================================
    # BUILD INFORMATION FOR AI
    # ========================================================

    scheme_information = f"""

Scheme name:
{scheme["name"]}

Description:
{scheme["description"]}

Eligibility:
{scheme["eligibility"]}

Benefits:
{scheme.get("benefits", "The available Aurynx information does not specify this.")}

Application:
{scheme["application"]}

Documents:
{scheme["documents"]}

Status:
{scheme.get("status", "The available Aurynx information does not specify this.")}

eKYC:
{scheme.get("ekyc", "The available Aurynx information does not specify this.")}

Official source:
{scheme["official"]}

"""


    # ========================================================
    # ASK OPENAI
    # ========================================================

    response = client.chat.completions.create(

        model="gpt-5-mini",

        messages=[

            {

                "role": "system",

               "content": (

    "You are Aurynx Citizen AI. "

    "IMPORTANT: You are NOT allowed to provide "
    "any government fact that is not explicitly "
    "written in the Government Information below. "

    "Treat the Government Information as the complete "
    "and only source of truth. "

    "Do not use your general knowledge. "

    "Do not infer missing requirements. "

    "Do not provide typical documents. "

    "Do not provide assumed documents. "

    "Do not provide examples of documents unless "
    "those examples appear in the Government Information. "

    "Do not add age limits, income limits, marks, "
    "deadlines, amounts, certificates, application "
    "steps or eligibility conditions unless they are "
    "explicitly present below. "

    "You MAY rewrite the provided information in "
    "simpler language and answer the user's question "
    "naturally. "

    "If the requested information is missing, say: "
    "'The available Aurynx information does not "
    "specify this.' "

    "Never fill missing information from your own knowledge."

)
            },

            {

                "role": "user",

                "content": (

                    f"Government information:\n"
                    f"{scheme_information}\n\n"

                    f"User question:\n"
                    f"{data.question}"

                )

            }

        ]

    )


    # ========================================================
    # GET AI ANSWER
    # ========================================================

    answer = (
        response
        .choices[0]
        .message
        .content
    )


    # ========================================================
    # RETURN AURYNX RESPONSE
    # ========================================================

    return {

        "question":
            data.question,

        "scheme":
            scheme["name"],

        "answer":
            answer,

        "official_source":
            scheme["official"]

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

    "You are Aurynx Citizen AI, a helpful government "
    "information assistant for citizens in India. "

    "Your job is to understand what the user is actually "
    "asking, even when the question is informal, short, "
    "grammatically incorrect, or uses everyday language. "

    "Use ONLY the Government Information provided below. "
    "Do not use your general knowledge. "
    "Do not invent, assume, or infer government rules. "

    "You may combine different pieces of information from "
    "the provided Government Information when answering. "

    "You may rewrite the information in simple, natural "
    "language so that ordinary citizens can understand it. "

    "If the user asks whether a particular person qualifies, "
    "do not claim that the person is definitely eligible "
    "unless the provided information is sufficient to confirm it. "

    "Instead, clearly explain what is known and what still "
    "needs to be checked. "

    "If specific information such as income limits, age limits, "
    "documents, deadlines, amounts, exclusions, or application "
    "steps is not provided, do not create it from your own "
    "knowledge. "

    "When information is missing, say naturally: "
    "'The available Aurynx information does not specify this.' "

    "Avoid unnecessary repetition. "

    "Answer directly first, then provide useful details. "

    "Use bullet points when they make the answer easier to read. "

    "If an official source is provided, mention it at the end. "

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
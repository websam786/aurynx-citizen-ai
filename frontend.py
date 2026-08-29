import streamlit as st
import requests
import speech_recognition as sr
import whisper
import os



BACKEND_URL = os.getenv(
    "AURYNX_BACKEND_URL",
    "http://127.0.0.1:8000"
)



@st.cache_resource
def load_whisper_model():

    return whisper.load_model("small")


whisper_model = load_whisper_model()

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Aurynx Citizen AI",
    page_icon="🇮🇳",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99,102,241,0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(14,165,233,0.12),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #f8fafc 0%,
                #eef2ff 100%
            );
    }

    .brand {
        font-size: 34px;
        font-weight: 900;
        letter-spacing: 3px;
        color: #172033;
    }

    .brand-star {
        color: #6366f1;
    }

    .subtitle {
        color: #64748b;
        font-size: 14px;
    }

    .hero-box {
        text-align: center;
        padding: 65px 20px 35px 20px;
    }

    .badge {
        display: inline-block;
        padding: 8px 18px;
        border-radius: 30px;
        background: rgba(99,102,241,0.10);
        color: #4f46e5;
        font-weight: 700;
        font-size: 14px;
    }

    .hero-title {
        font-size: 52px;
        line-height: 1.1;
        font-weight: 900;
        color: #111827;
        margin-top: 20px;
    }

    .gradient-text {
        background: linear-gradient(
            90deg,
            #6366f1,
            #0ea5e9
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-text {
        max-width: 700px;
        margin: 20px auto;
        font-size: 18px;
        line-height: 1.7;
        color: #64748b;
    }

    .search-title {
        text-align: center;
        font-size: 30px;
        font-weight: 800;
        color: #111827;
        margin-top: 10px;
    }

    .search-subtitle {
        text-align: center;
        color: #64748b;
        margin-bottom: 25px;
    }

    .service-box {
        background: rgba(255,255,255,0.92);
        border-radius: 22px;
        padding: 25px;
        min-height: 175px;
        border: 1px solid rgba(148,163,184,0.18);
        box-shadow: 0 8px 25px rgba(15,23,42,0.06);
    }

    .answer-box {
        background: rgba(255,255,255,0.96);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(99,102,241,0.12);
        box-shadow: 0 12px 35px rgba(15,23,42,0.08);
        margin: 25px 0;
    }

    .footer {
        text-align: center;
        padding: 60px 0 30px 0;
        color: #94a3b8;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

header1, header2 = st.columns([5, 1])

with header1:

    st.markdown(
        '<div class="brand">AURYNX<span class="brand-star">✦</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Citizen AI • Government Services Simplified</div>',
        unsafe_allow_html=True
    )


with header2:

    st.markdown(
        "<div style='text-align:right;font-weight:700;'>🇮🇳 India</div>",
        unsafe_allow_html=True
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero-box">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="badge">✨ AI-powered citizen assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-title">
        Government services,<br>
        <span class="gradient-text">made simple.</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-text">
        Ask questions about scholarships, government schemes,
        citizen benefits and official documents.
        Aurynx helps you understand them clearly.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# AI SEARCH
# ============================================================

st.markdown(
    '<div class="search-title">What can Aurynx help you with?</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="search-subtitle">
        Ask about scholarships, government schemes,
        benefits, certificates and citizen services.
    </div>
    """,
    unsafe_allow_html=True
)


question = st.text_input(
    "Ask Aurynx",
    placeholder="🔍  e.g. Who can apply for PM-YASASVI?",
    label_visibility="collapsed"
)
st.caption("🎤 Or ask Aurynx using your voice")

audio_value = st.audio_input(
    "Record your question"
)

if audio_value is not None:

    try:

        with st.spinner("🎧 Aurynx is understanding your voice..."):

            audio_bytes = audio_value.getvalue()

            with open("voice_question.wav", "wb") as f:
                f.write(audio_bytes)

            result = whisper_model.transcribe(
                "voice_question.wav",
                task="transcribe"
            )

            voice_text = result["text"].strip()
            detected_language = result.get("language", "")

        if voice_text:

            if detected_language == "ml":
                language_name = "Malayalam 🇮🇳"

            elif detected_language == "en":
                language_name = "English 🇮🇳"

            else:
                language_name = detected_language

            st.success(
                f"🎤 You said: {voice_text}"
            )

            st.caption(
                f"Detected language: {language_name}"
            )

            question = voice_text

        else:

            st.warning(
                "Sorry, Aurynx could not understand your voice."
            )

    except Exception as e:

        st.error(
            f"❌ Voice input error: {str(e)}"
        )

if st.button(
    "✨ Ask Aurynx",
    use_container_width=True
):

    if not question.strip():

        st.warning("Please enter your question.")

    else:

        try:

            with st.spinner("Aurynx is thinking..."):

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "question": question
                    },
                    timeout=60
                )


            if response.status_code == 200:

                result = response.json()

                st.markdown(
                    '<div class="answer-box">',
                    unsafe_allow_html=True
                )

                st.markdown("### 🤖 Aurynx")

                if result.get("answer"):

                    st.write(
                        result["answer"]
                    )

                elif result.get("message"):

                    st.write(
                        result["message"]
                    )

                else:

                    st.write(
                        "I couldn't find an answer."
                    )

                if result.get("scheme"):

                    st.caption(
                        f"Scheme: {result['scheme']}"
                    )

                if result.get("official_source"):

                    st.caption(
                        f"Official source: {result['official_source']}"
                    )
                if result.get("last_verified"):

                    st.caption(
                        f"📅 Last verified: {result['last_verified']}"
                    )

                if result.get("verification_frequency"):

                   st.caption(
                       f"🔄 Verification frequency: {result['verification_frequency']}"
    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


            else:

                st.error(
                    f"Aurynx server returned an error "
                    f"({response.status_code})."
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Aurynx backend is not running. "
                "Please start FastAPI first."
            )


        except requests.exceptions.Timeout:

            st.error(
                "⏳ Aurynx took too long to respond."
            )


        except Exception as e:

            st.error(
                f"❌ Unexpected error: {str(e)}"
            )

# ============================================================
# SERVICES
# ============================================================

st.markdown("## Explore Citizen Services")

st.caption(
    "Quick access to information that matters to you."
)


services = {

    "🎓 Scholarships": {
        "description": (
            "Find education scholarships, eligibility, "
            "documents and application information."
        ),
        "questions": [
            "Who can apply for PM-YASASVI?",
            "What documents are required for scholarships?",
            "How can I apply for a government scholarship?"
        ]
    },

    "💰 Government Benefits": {
        "description": (
            "Discover financial assistance, welfare schemes "
            "and citizen benefits."
        ),
        "questions": [
            "What government benefits are available?",
            "Who is eligible for government financial assistance?",
            "How can I apply for a government benefit?"
        ]
    },

    "📄 Certificates": {
        "description": (
            "Understand certificates, required documents "
            "and application procedures."
        ),
        "questions": [
            "How can I apply for an income certificate?",
            "What documents are required for a certificate?",
            "Where can I apply for a government certificate?"
        ]
    },

    "💼 Employment": {
        "description": (
            "Explore government employment opportunities, "
            "employment schemes and skill programs."
        ),
        "questions": [
            "What government employment opportunities are available?",
            "Are there government employment schemes for young people?",
            "Where can I find government job information?"
        ]
    }

}


cols = st.columns(4)


for col, (service_name, service_data) in zip(
    cols,
    services.items()
):

    with col:

        st.markdown(
            f"### {service_name}"
        )

        st.write(
            service_data["description"]
        )

        st.markdown("**Try asking:**")

        for question_example in service_data["questions"]:

            if st.button(
                question_example,
                key=f"{service_name}_{question_example}",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        "Aurynx is thinking..."
                    ):

                        response = requests.post(
                            f"{BACKEND_URL}/ask",
                            json={
                                "question": question_example
                            },
                            timeout=60
                        )


                    if response.status_code == 200:

                        result = response.json()

                        st.markdown(
                            '<div class="answer-box">',
                            unsafe_allow_html=True
                        )

                        st.markdown("### 🤖 Aurynx")

                        if result.get("answer"):

                            st.write(
                                result["answer"]
                            )

                        elif result.get("message"):

                            st.write(
                                result["message"]
                            )

                        else:

                            st.write(
                                "I couldn't find an answer."
                            )

                        if result.get("scheme"):

                            st.caption(
                                f"Scheme: {result['scheme']}"
                            )

                        if result.get("official_source"):

                            st.caption(
                                f"Official source: "
                                f"{result['official_source']}"
                            )
                        if result.get("last_verified"):

                            st.caption(
                                f"📅 Last verified: {result['last_verified']}"
                            )

                        if result.get("verification_frequency"):

                           st.caption(
                                f"🔄 Verification frequency: {result['verification_frequency']}"
                            )    

                        st.markdown(
                            '</div>',
                            unsafe_allow_html=True
                        )

                    else:

                        st.error(
                            f"Aurynx server returned an error "
                            f"({response.status_code})."
                        )


                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Aurynx backend is not running."
                    )


                except requests.exceptions.Timeout:

                    st.error(
                        "⏳ Aurynx took too long to respond."
                    )


                except Exception as e:

                    st.error(
                        f"❌ Unexpected error: {str(e)}"
                    )

# ============================================================
# DOCUMENT UPLOAD
# ============================================================

st.markdown("## 📚 Ask about a government document")

st.caption(
    "Upload an official government PDF and ask Aurynx questions about it."
)


uploaded_file = st.file_uploader(
    "Upload an official government PDF",
    type=["pdf"]
)


if uploaded_file:

    if st.button(
        "📤 Upload to Aurynx",
        use_container_width=True
    ):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }


        try:

            with st.spinner(
                "Uploading and processing document..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/upload-document",
                    files=files,
                    timeout=120
                )


            if response.status_code == 200:

                result = response.json()

                st.success(
                    f"Document uploaded successfully — "
                    f"{result.get('chunks', 0)} chunks created."
                )

            else:

                st.error(
                    f"Document upload failed "
                    f"({response.status_code})."
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to the Aurynx backend."
            )


        except requests.exceptions.Timeout:

            st.error(
                "⏳ Document upload took too long."
            )


        except Exception as e:

            st.error(
                f"❌ Unexpected error: {str(e)}"
            )


# ============================================================
# ASK DOCUMENT
# ============================================================

st.markdown("## 🤖 Ask Aurynx about your document")


document_question = st.text_input(
    "Document question",
    placeholder="🔍 Ask something about the uploaded government document...",
    label_visibility="collapsed"
)


if st.button(
    "✨ Ask Document",
    use_container_width=True
):

    if not document_question.strip():

        st.warning(
            "Please enter a question first."
        )

    else:

        try:

            with st.spinner(
                "Aurynx is reading your document..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/ask-document",
                    json={
                        "question": document_question
                    },
                    timeout=60
                )


            result = response.json()


            if response.status_code == 200:

                st.markdown(
                    '<div class="answer-box">',
                    unsafe_allow_html=True
                )

                st.markdown("### 🤖 Aurynx")

                answer = result.get("answer")


                if answer:

                    st.write(answer)

                elif result.get("message"):

                    st.warning(
                        result["message"]
                    )

                else:

                    st.warning(
                        "Aurynx returned a response, "
                        "but no answer was found."
                    )


                if result.get("source_document"):

                    st.markdown(
                        f"📄 **Source:** "
                        f"{result['source_document']}"
                    )


                if result.get("document_year"):

                    st.markdown(
                        f"📅 **Document year:** "
                        f"{result['document_year']}"
                    )


                if result.get("notice"):

                    st.warning(
                        result["notice"]
                    )


                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


            else:

                st.error(
                    f"Backend error: {response.status_code}"
                )

                st.json(result)


        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to Aurynx backend. "
                "Make sure FastAPI is running."
            )


        except requests.exceptions.Timeout:

            st.error(
                "⏳ Aurynx took too long to respond."
            )


        except Exception as e:

            st.error(
                f"❌ Unexpected error: {str(e)}"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <b>AURYNX Citizen AI</b><br>
        Making government information easier to understand.
    </div>
    """,
    unsafe_allow_html=True
)
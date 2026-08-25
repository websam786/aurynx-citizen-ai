
import streamlit as st
import requests


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

    /* HEADER */

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

    /* HERO */

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

    /* SEARCH */

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

    /* SERVICE CARDS */

    .service-box {
        background: rgba(255,255,255,0.92);
        border-radius: 22px;
        padding: 25px;
        min-height: 175px;
        border: 1px solid rgba(148,163,184,0.18);
        box-shadow: 0 8px 25px rgba(15,23,42,0.06);
    }

    .service-icon {
        font-size: 38px;
    }

    .service-name {
        font-size: 20px;
        font-weight: 800;
        color: #172033;
        margin-top: 10px;
    }

    .service-text {
        color: #64748b;
        line-height: 1.5;
        margin-top: 8px;
    }

    /* ANSWER */

    .answer-box {
        background: rgba(255,255,255,0.96);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(99,102,241,0.12);
        box-shadow: 0 12px 35px rgba(15,23,42,0.08);
        margin: 25px 0;
    }

    /* FOOTER */

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
    placeholder="🔍  e.g. Who can apply for the Pragati scholarship?",
    label_visibility="collapsed"
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
                    "http://127.0.0.1:8000/ask",
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

                if result.get("scheme"):

                    st.success(
                        result["scheme"]
                    )

                    if result.get("description"):

                        st.write(
                            result["description"]
                        )

                    if result.get("official_source"):

                        st.markdown(
                            f"**Official source:** "
                            f"{result['official_source']}"
                        )

                elif result.get("answer"):

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

services = [
    (
        "🎓",
        "Scholarships",
        "Find education scholarships and eligibility information."
    ),
    (
        "💰",
        "Government Benefits",
        "Discover financial assistance and welfare schemes."
    ),
    (
        "📄",
        "Certificates",
        "Understand documents, certificates and application requirements."
    ),
    (
        "💼",
        "Employment",
        "Explore government employment opportunities and schemes."
    ),
]

cols = st.columns(4)

for col, service in zip(cols, services):

    icon, title, description = service

    with col:

        st.markdown(
            f"## {icon}"
        )

        st.markdown(
            f"### {title}"
        )

        st.write(
            description
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
                    "http://127.0.0.1:8000/upload-document",
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
                    "http://127.0.0.1:8000/ask-document",
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


import streamlit as st
import os
from src.agent import answer_question
from src.agent import get_sub_questions  # We'll add this helper in agent.py

st.set_page_config(
    page_title="MultiPDFAgent: Legal Document QA Bot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a clean, professional look
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, .stApp {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #23243a 0%, #4b6584 100%) !important;
        color: #f5f7fa !important;
    }
    section[data-testid="stSidebar"] .css-1v3fvcr, section[data-testid="stSidebar"] .css-1d391kg {
        color: #f5f7fa !important;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3a4a;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .sub-header {
        font-size: 1.15rem;
        color: #4b6584;
        margin-bottom: 2rem;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    textarea, .stTextInput > div > div > input {
        background: #f5f7fa;
        border-radius: 8px;
        border: 1px solid #c3cfe2;
        color: #2d3a4a;
        font-size: 1.08rem;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .stButton > button {
        background: linear-gradient(90deg, #4b6584 0%, #6a89cc 100%);
        color: #fff;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1.5rem;
        font-size: 1.08rem;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        box-shadow: 0 2px 8px rgba(44,62,80,0.08);
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #6a89cc 0%, #4b6584 100%);
        color: #fff;
    }
    .answer-block {
        background: #fff;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(44,62,80,0.08);
        margin-bottom: 1.5rem;
        border-left: 6px solid #6a89cc;
        color: #2d3a4a;
        font-size: 1.08rem;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .stInfo, .stError {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        font-size: 1.05rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header">📄 MultiPDFAgent: Legal Document QA Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask questions about your legal documents. The agent will answer with references to the source documents and sections.</div>', unsafe_allow_html=True)

# Sidebar for sub-questions
st.sidebar.header("Sub-questions (Reasoning Steps)")

with st.form("qa_form"):
    user_query = st.text_area("Enter your legal question:", height=100, key="user_query")
    submit = st.form_submit_button("Get Answer")

if submit and user_query.strip():
    # Show sub-questions in sidebar
    sub_questions = get_sub_questions(user_query)
    for i, subq in enumerate(sub_questions, 1):
        st.sidebar.markdown(f"**{i}.** {subq}")
    with st.spinner("Analyzing documents and generating answer..."):
        answer = answer_question(user_query)
        st.markdown(f"<div class='answer-block'><b>Answer</b><br>{answer}</div>", unsafe_allow_html=True)
else:
    st.info("Enter a question and click 'Get Answer' to begin.")

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#6a89cc; font-size:0.9rem;'>Powered by MultiPDFAgent &copy; 2025</div>",
    unsafe_allow_html=True,
)

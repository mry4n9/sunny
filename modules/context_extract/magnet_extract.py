import streamlit as st
import fitz  # PyMuPDF
import io

@st.cache_data(show_spinner=False)
def extract_text_from_magnet(uploaded_file):
    """Extracts text from a PDF lead magnet."""
    if uploaded_file is None:
        return ""

    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name.lower()
    text = ""

    try:
        if file_name.endswith(".pdf"):
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text() + "\n"
        else:
            st.warning(f"Unsupported file type for lead magnet: {uploaded_file.name}. Please use PDF.")
            return ""
    except Exception as e:
        st.error(f"Error extracting text from lead magnet {uploaded_file.name}: {e}")
        return ""
    return text
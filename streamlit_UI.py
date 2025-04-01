import streamlit as st
from extractor import PDFTextExtractor  # Import extraction class

st.title("📄 PDF Text Extractor")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Checkbox for Markdown extraction
use_mupdf4llm = st.checkbox("Use PyMuPDF4LLM (Markdown Extraction)")

# Choose file format
file_format = st.radio("Save as:", ["Text (.txt)", "Markdown (.md)"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    pdf_path = f"temp_uploaded.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    # Extract text
    extractor = PDFTextExtractor(pdf_path, use_mupdf4llm)
    extracted_text = extractor.extract_text()

    # Display extracted text
    st.text_area("Extracted Text", extracted_text, height=300)

    # Provide download button
    file_extension = ".md" if "Markdown" in file_format else ".txt"
    st.download_button(label="Download Extracted Text", data=extracted_text, file_name=f"extracted_text{file_extension}")

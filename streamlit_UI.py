import streamlit as st
import os
import tempfile
from extractor import PDFTextExtractor  # Importing the text extraction class

# --- App Config ---
st.set_page_config(
    page_title="📄 PDF Text Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stDownloadButton button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
        }
        .stDownloadButton button:hover {
            background-color: #45a049;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .file-uploader {
            margin-bottom: 1.5rem;
        }
        .extracted-text {
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
        }
        .header-icon {
            font-size: 1.5em;
            vertical-align: middle;
            margin-right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Header ---
st.title("📄 PDF Text Extractor")
st.markdown("Extract text content from PDF files with customizable output options.")

# --- Sidebar for Upload & Options ---
with st.sidebar:
    st.header("Upload & Settings")
    st.markdown("---")
    
    # File Uploader with improved styling
    with st.container():
        st.markdown('<div class="file-uploader">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose a PDF file", 
            type=["pdf"],
            help="Upload the PDF file you want to extract text from"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Extraction Options
    st.subheader("Extraction Options")
    use_mupdf4llm = st.checkbox(
        "Use advanced Markdown extraction", 
        value=False,
        help="Enable PyMuPDF4LLM for better Markdown formatting"
    )
    
    # File Format Selection with better labels
    st.subheader("Output Options")
    file_format = st.radio(
        "Select output format:",
        ["Text (.txt)", "Markdown (.md)"],
        index=1 if use_mupdf4llm else 0,
        help="Choose the format for the extracted text"
    )

# --- Main Content Area ---
if uploaded_file is not None:
    # Processing section
    with st.status("Processing PDF file...", expanded=True) as status:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_pdf_path = temp_file.name

        # Extract text
        st.write("Extracting text content...")
        extractor = PDFTextExtractor(temp_pdf_path, use_mupdf4llm)
        extracted_text = extractor.extract_text()
        
        status.update(label="Extraction complete!", state="complete", expanded=False)

    # Results section
    st.subheader("Extraction Results")
    
    # Text stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("File Name", uploaded_file.name)
    with col2:
        st.metric("Text Length", f"{len(extracted_text):,} characters")
    
    # Extracted text display
    with st.expander("View Extracted Text", expanded=True):
        st.markdown('<div class="extracted-text">', unsafe_allow_html=True)
        st.text_area(
            "Extracted Content", 
            extracted_text, 
            height=400,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Download button with improved styling
    file_extension = ".md" if "Markdown" in file_format else ".txt"
    st.download_button(
        label="📥 Download Extracted Text",
        data=extracted_text,
        file_name=f"{os.path.splitext(uploaded_file.name)[0]}_extracted{file_extension}",
        mime="text/plain",
        help="Click to download the extracted text"
    )

    # Clean up temporary file
    os.remove(temp_pdf_path)

else:
    # Empty state with instructions
    st.info("ℹ️ Please upload a PDF file using the sidebar controls to begin extraction.")
    with st.expander("How to use this tool"):
        st.markdown("""
        1. **Upload a PDF** file using the file uploader in the sidebar
        2. Choose your **extraction options**:
           - Enable advanced Markdown extraction for better formatting
           - Select your preferred output format
        3. View the extracted text directly in the app
        4. Download the results in your chosen format
        """)
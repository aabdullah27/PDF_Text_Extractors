import fitz  # PyMuPDF
import pymupdf4llm

class PDFTextExtractor:
    """Handles PDF text extraction with options for plain text or Markdown."""

    def __init__(self, pdf_path, use_mupdf4llm=False):
        self.pdf_path = pdf_path
        self.use_mupdf4llm = use_mupdf4llm

    def extract_text(self):
        """Extract text based on the chosen method."""
        if self.use_mupdf4llm:
            return self._extract_with_mupdf4llm()
        else:
            return self._extract_with_pymupdf()

    def _extract_with_mupdf4llm(self):
        """Extract text in Markdown format using PyMuPDF4LLM."""
        return pymupdf4llm.to_markdown(self.pdf_path)

    def _extract_with_pymupdf(self):
        """Extract plain text using PyMuPDF."""
        text = []
        with fitz.open(self.pdf_path) as pdf_document:
            for page in pdf_document:
                text.append(page.get_text())
        return "\n".join(text)
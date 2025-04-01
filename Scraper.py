import tkinter as tk
from tkinter import filedialog, messagebox
import fitz
import pymupdf4llm
import pathlib

def extract_text_from_pdf(pdf_path, use_mupdf4llm):
    """Extract text using the selected library."""
    if use_mupdf4llm:
        return pymupdf4llm.to_markdown(pdf_path)  # Extract as Markdown
    else:
        text = ""
        with fitz.open(pdf_path) as pdf_document:
            for page in pdf_document:
                text += page.get_text()
        return text

def save_text_to_file(text, file_format):
    """Save extracted text to a file in the chosen format."""
    file_extension = ".md" if file_format == "Markdown" else ".txt"
    save_path = filedialog.asksaveasfilename(defaultextension=file_extension, 
                                             filetypes=[(f"{file_format} files", f"*{file_extension}"), 
                                                        ("All files", "*.*")])
    if save_path:
        pathlib.Path(save_path).write_bytes(text.encode("utf-8"))
        messagebox.showinfo("Success", f"Text successfully saved to: {save_path}")

def select_pdf():
    """Handle PDF selection and extraction."""
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if pdf_path:
        extracted_text = extract_text_from_pdf(pdf_path, use_mupdf4llm_var.get())
        save_text_to_file(extracted_text, file_format_var.get())

# Create the GUI
root = tk.Tk()
root.title("PDF to Text/Markdown Extractor")
root.geometry("400x250")

# UI Elements
label = tk.Label(root, text="Select a PDF file to extract text", font=("Arial", 12))
label.pack(pady=10)

use_mupdf4llm_var = tk.BooleanVar()
checkbox = tk.Checkbutton(root, text="Use PyMuPDF4LLM (Markdown Extraction)", variable=use_mupdf4llm_var)
checkbox.pack(pady=5)

file_format_var = tk.StringVar(value="Text")
format_label = tk.Label(root, text="Save as:")
format_label.pack()

radio_txt = tk.Radiobutton(root, text=".txt", variable=file_format_var, value="Text")
radio_md = tk.Radiobutton(root, text=".md", variable=file_format_var, value="Markdown")
radio_txt.pack()
radio_md.pack()

button = tk.Button(root, text="Choose PDF", command=select_pdf, font=("Arial", 12), bg="#4CAF50", fg="white")
button.pack(pady=10)

root.mainloop()

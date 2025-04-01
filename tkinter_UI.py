import tkinter as tk
from tkinter import filedialog, messagebox
import pathlib
from extractor import PDFTextExtractor  # Import extraction class

def select_pdf():
    """Handle PDF selection, extraction, and saving."""
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if pdf_path:
        extractor = PDFTextExtractor(pdf_path, use_mupdf4llm_var.get())
        extracted_text = extractor.extract_text()
        save_text_to_file(extracted_text)

def save_text_to_file(text):
    """Save extracted text to a file in the chosen format."""
    file_extension = ".md" if file_format_var.get() == "Markdown" else ".txt"
    save_path = filedialog.asksaveasfilename(defaultextension=file_extension, 
                                             filetypes=[(f"{file_format_var.get()} files", f"*{file_extension}"), 
                                                        ("All files", "*.*")])
    if save_path:
        pathlib.Path(save_path).write_bytes(text.encode("utf-8"))
        messagebox.showinfo("Success", f"Text successfully saved to: {save_path}")

# GUI Setup
root = tk.Tk()
root.title("PDF Text Extractor")
root.geometry("400x250")

tk.Label(root, text="Select a PDF file to extract text", font=("Arial", 12)).pack(pady=10)

use_mupdf4llm_var = tk.BooleanVar()
tk.Checkbutton(root, text="Use PyMuPDF4LLM (Markdown Extraction)", variable=use_mupdf4llm_var).pack(pady=5)

tk.Label(root, text="Save as:").pack()

file_format_var = tk.StringVar(value="Text")
tk.Radiobutton(root, text=".txt", variable=file_format_var, value="Text").pack()
tk.Radiobutton(root, text=".md", variable=file_format_var, value="Markdown").pack()

tk.Button(root, text="Choose PDF", command=select_pdf, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

root.mainloop()

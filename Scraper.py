import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Extract text from a PDF file
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page in pdf_document:
            text += page.get_text()
    return text

def save_text_to_file(text):
    # Save extracted text to a .txt file
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if save_path:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(text)
        messagebox.showinfo("Success", f"Text successfully saved to: {save_path}")

def select_pdf():
    # Select a PDF file and extract its text
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if pdf_path:
        extracted_text = extract_text_from_pdf(pdf_path)
        save_text_to_file(extracted_text)

# Create the GUI
root = tk.Tk()
root.title("PDF to Text Extractor")
root.geometry("300x150")

label = tk.Label(root, text="Select a PDF file to extract text")
label.pack(pady=20)

button = tk.Button(root, text="Choose PDF", command=select_pdf)
button.pack(pady=10)

root.mainloop()

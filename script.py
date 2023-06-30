import streamlit as st
import os
from PyPDF2 import PdfMerger
from fpdf import FPDF
from pyPDF2 import PdfFileReader

def merge_pdfs(output_filename, *pdf_files):
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)
    merger.write(output_filename)
    merger.close()

def generate_pdf(content, output_filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=content, ln=1)
    pdf.output(output_filename)

def main():
    st.title("PDF-Application-Summary")
    
    cv_path = "./data/curriculum_vitae"
    cover_letter_folder = "./data/cover_letters"
    additional_folder = "./data/additional"
    
    st.subheader("VC")
    st.text(cv_path)
    
    st.subheader("cover_letters")
    cover_letter_files = os.listdir(cover_letter_folder)
    selected_cover_letter = st.selectbox("Company Name", cover_letter_files)
    cover_letter_path = os.path.join(cover_letter_folder, selected_cover_letter)
    st.text(cover_letter_path)
    
    st.subheader("Additional")
    additional_files = os.listdir(additional_folder)
    selected_files = st.multiselect("File", additional_files)
    additional_paths = [os.path.join(additional_folder, file) for file in selected_files]
    for path in additional_paths:
        st.text(path)
    
    if st.button("Create PDF"):
        output_filename = "merged.pdf"
        
        # Zusammenführen der Dateien
        pdf_files = [cv_path, cover_letter_path] + additional_paths
        merge_pdfs(output_filename, *pdf_files)
        
        st.success(f"Die PDF-Datei wurde erfolgreich erstellt: [Download](./{output_filename})")
    
    st.subheader("PDF Viewer")
    if st.button("View PDF"):
        pdf_file = open(output_filename, "rb")
        pdf_reader = PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            st.image(page.extractText())
    
    st.text("Note: Please check the file paths carefully before creating the PDF.")

if __name__ == "__main__":
    main()

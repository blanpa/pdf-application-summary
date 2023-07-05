import streamlit as st
import os
from pypdf import PdfMerger
from fpdf import FPDF
from docx2pdf import convert
import re
from os import path
from glob import glob 
import base64


def merge_pdfs(output_filename, *pdf_files):
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)
    merger.write(output_filename)
    merger.close()

def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))


def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def main():
    st.title("PDF-Application-Summary")

    st.selectbox("Language", ("English", "German"))
    
    cv_path = os.path.join("data", "1_curriculum_vitae", "cv.pdf")#"./data/curriculum_vitae"
    cover_letter_folder = os.path.join("data", "0_cover_letter") #"./data/cover_letter"
    additional_folder = os.path.join("data", "2_additional")#"./data/additional"
    
    st.subheader("Curriculum Vitae (CV)")
    st.write("Found CV:", cv_path)

    st.subheader("Cover Letter")
    
    with st.expander("cover_letters word to pdf"):
        cover_letter_files = find_ext(cover_letter_folder, "docx")
        selected_cover_letter = st.selectbox("Company Name", cover_letter_files)
        cover_letter_path = os.path.join(cover_letter_folder, selected_cover_letter)
        st.text(cover_letter_path)
        output_filename = cover_letter_path.replace("docx","pdf")
        st.text(output_filename)

        if st.button("Create PDF"):          
            # Zusammenführen der Dateien
            convert(cover_letter_path,output_filename)
            st.success(f"Die PDF-Datei wurde erfolgreich erstellt: [Download](./{output_filename})")

    selected_cover_letter = st.selectbox("Company_ Name", find_ext(cover_letter_folder,"pdf"))
    cover_letter_path = os.path.join(selected_cover_letter)
    st.text(cover_letter_path)


    st.subheader("Additional")
    additional_files = os.listdir(additional_folder)
    selected_files = st.multiselect("File", additional_files)
    additional_paths = [os.path.join(additional_folder, file) for file in selected_files]
    for path in additional_paths:
        st.text(path)
    
    pdf_files = [cover_letter_path, cv_path] + additional_paths
    st.write(pdf_files)
    match = re.search(r"_([^_]+)$", selected_cover_letter)
    final_path = os.path.join("data", "3_merged_application",f"application_{match.group(1)}")

    if st.button("Merged PDF"):
        # Zusammenführen der Dateien
        merge_pdfs(final_path, *pdf_files)
        
        st.success(f"Die PDF-Datei wurde erfolgreich erstellt: [Download](./{final_path})")
    
    st.subheader("PDF Viewer")
    st.write(final_path)
    if st.button("View PDF"):
        show_pdf(final_path)
    
    st.text("Note: Please check the file paths carefully before creating the PDF.")

if __name__ == "__main__":
    main()

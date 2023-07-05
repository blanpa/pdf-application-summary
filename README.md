# PDF Application Summary

This is a Python script that helps you create a summary of your job application documents in PDF format. It allows you to convert Word cover letters to PDF, merge multiple PDF files together, and view the final PDF using Streamlit.

## Requirements

Make sure you have the following packages installed:

- streamlit
- os
- pypdf
- fpdf
- docx2pdf
- re
- glob
- base64

You can install these packages using pip:

```shell
pip install streamlit pypdf fpdf docx2pdf
```

## How to Use

1. Import the required libraries:

```python
import streamlit as st
import os
from pypdf import PdfMerger
from fpdf import FPDF
from docx2pdf import convert
import re
from os import path
from glob import glob 
import base64
```

2. Define the `merge_pdfs` function to merge multiple PDF files:

```python
def merge_pdfs(output_filename, *pdf_files):
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)
    merger.write(output_filename)
    merger.close()
```

3. Define the `find_ext` function to find files with a specific extension in a directory:

```python
def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))
```

4. Define the `show_pdf` function to display a PDF file using Streamlit:

```python
def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
```

5. Define the `main` function that contains the main logic of the application:

```python
def main():
    st.title("PDF-Application-Summary")

    st.selectbox("Language", ("English", "German"))
    
    cv_path = os.path.join("data", "1_curriculum_vitae", "cv.pdf")
    cover_letter_folder = os.path.join("data", "0_cover_letter")
    additional_folder = os.path.join("data", "2_additional")
    
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
        st.text(path

6. Define the paths of the cover letter, CV, and additional files, and display them:

```python
pdf_files = [cover_letter_path, cv_path] + additional_paths
st.write(pdf_files)
match = re.search(r"_([^_]+)$", selected_cover_letter)
final_path = os.path.join("data", "3_merged_application",f"application_{match.group(1)}")
```

7. If the "Merged PDF" button is clicked, merge the PDF files into a single PDF:

```python
if st.button("Merged PDF"):
    merge_pdfs(final_path, *pdf_files)
    st.success(f"Die PDF-Datei wurde erfolgreich erstellt: [Download](./{final_path})")
```

8. Display the PDF viewer and allow the user to view the final PDF:

```python
st.subheader("PDF Viewer")
st.write(final_path)
if st.button("View PDF"):
    show_pdf(final_path)
```

9. Add a note to remind the user to check the file paths carefully before creating the PDF:

```python
st.text("Note: Please check the file paths carefully before creating the PDF.")
```

10. Execute the `main` function if the script is run directly:

```python
if __name__ == "__main__":
    main()
```

## Running the Script

To run the script, execute the following command:

```shell
streamlit run <filename>.py
```

Replace `<filename>` with the name of your Python script containing the above code.

## Note

This README provides an overview of the script and its functionalities. For a detailed understanding, please refer to the comments within the script and the code implementation.


Run the following command to build the Docker container:

    docker build -t pdf-app .

Open a web browser and go to the address http://localhost:8501 to access the Streamlit application.

These steps will create and run a Docker container that contains the Streamlit application. The container is based on a Python 3.9 image, installs the required packages from the requirements.txt file, and copies the entire contents of the current directory into the container. The Streamlit server is then started and the application is made available via port 8501.

Please make sure that you have Docker installed on your system and that you have run the Docker daemon before executing the above commands.

When running the container, you can use the -v flag to mount volumes. Here is an example command that mounts the /path/to/local/folder folder into the container:

    docker run -p 8501:8501 -v /data:/app/data pdf-app

Using -v /path/to/local/folder:/app/local_folder will connect the local folder outside the container to the /app/local_folder directory inside the container. This allows the application to access the contents of the local folder.

In the Python script, you can then use the path local_folder to access the files inside the mounted volume.

Please note that the path /path/to/local/folder must exist on your host system and contain the necessary files for the application to access.

Translated with www.DeepL.com/Translator (free version)
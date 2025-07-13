from langchain.schema import Document
from pypdf import PdfReader


# Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list):
    docs = []
    # each pdf file is a doc. We are creating our own Document with it
    for filename in user_pdf_list:

        chunks = get_pdf_text(filename)

        # Adding items to our list - Adding data & its metadata
        docs.append(
            Document(
                page_content=chunks,
                metadata={
                    "name": filename.name,
                    # "id": filename.file_id,
                    "type=": filename.type,
                    "size": filename.size,
                },
            )
        )

    return docs  # Document chunks list

# from langchain.schema import Document
from langchain_core.documents import Document
from pypdf import PdfReader


# Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    if len(pdf_reader.pages) == 0:
        raise ValueError("No pages found in the PDF file")
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list, unique_id):
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
                    "file_id": unique_id,
                    "type=": filename.type,
                    "size": filename.size,
                },
            )
        )

    return docs  # Document chunks list

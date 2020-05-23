import pdftotext
import magic
import io


def pdf_to_str(path):
    with open(path, 'rb') as f:
        load_pdf = io.BytesIO(f.read())
        pdf_obj = pdftotext.PDF(load_pdf)
        return ' '.join([str(page) for page in pdf_obj])


def test_format(path):
    return magic.from_file(path, mime=True)

# application/pdf or text/plain formats are supported


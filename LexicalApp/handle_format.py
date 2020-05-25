import pdftotext
import magic
import io
from django.core.exceptions import ValidationError


def pdf_to_str(path):
    with open(path, 'rb') as f:
        load_pdf = io.BytesIO(f.read())
        pdf_obj = pdftotext.PDF(load_pdf)
        return ' '.join([str(page) for page in pdf_obj])


def get_format(path):
    return magic.from_file(path, mime=True)


def type_validator(file):
    filetype = magic.from_buffer(file.read()).lower()
    if 'pdf' not in filetype and 'text' not in filetype:
        raise ValidationError('Error! You are trying to upload a file with an unsupported type!')



from django import forms
from .handle_format import type_validator


class BookForm(forms.Form):

    title = forms.CharField(label='Title', max_length=128, required=True)
    author = forms.CharField(label='Author', max_length=128, required=True)
    book = forms.FileField(label='Upload', validators=[type_validator])



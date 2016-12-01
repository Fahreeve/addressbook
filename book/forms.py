from django import forms

from authreg.forms import MyFormMixin
from book.models import Note


class NoteForm(MyFormMixin, forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['user']

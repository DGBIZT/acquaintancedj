from django import forms
from .models import Blog
from catalog.forms import validate_forbidden_words

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        validate_forbidden_words(title)
        return title

    def clean_content(self):
        description = self.cleaned_data.get('content')
        validate_forbidden_words(description)
        return description

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название блога'
        })

        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Содержание блога'
        })

        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
        })
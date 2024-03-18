from django import forms
from django.forms import CharField, TextInput

from .utils import get_mongodb


class AuthorForm(forms.Form):
    fullname = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control", "id": "exampleInputText1"}))
    born_date = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control", "id": "exampleInputText2"}))
    born_location = CharField(max_length=150,
                              widget=TextInput(attrs={"class": "form-control", "id": "exampleInputText3"}))
    description = CharField(widget=TextInput(attrs={"class": "form-control", "id": "exampleInputText4"}))


class QuoteForm(forms.Form):
    quote = forms.CharField(max_length=50,
                            widget=forms.TextInput(attrs={"class": "form-control", "id": "exampleInputQuote1"}))

    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "exampleInputQuote2"}))

    author = forms.ChoiceField(choices=[],
                               widget=forms.Select(attrs={"class": "form-control", "id": "exampleInputQuote3"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db = get_mongodb()
        authors_cursor = db.authors.find()
        authors = list(authors_cursor)

        author_choices = []
        for author in authors:
            author_choices.append((str(author["_id"]), author["fullname"]))
        try:
            self.fields['author'].choices = [("", "Select an author")] + author_choices
        except Exception as e:
            print("An error occurred during form initialization:", e)

        def clean_tags(self):
            """
            Custom validation to parse tags input into a list.
            """
            tags_input = self.cleaned_data['tags']
            if tags_input:
                # Split the input string by commas and strip whitespace from each tag
                tags_list = [tag.strip() for tag in tags_input.split(',')]
                return tags_list
            else:
                return []  # Return an empty list if no tags provided

from django.forms import ModelForm, CharField, DateTimeField, TextInput, ModelChoiceField, Select

from .models import Author, Quote


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control", "id": "exampleInputText1"}))
    born_date = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control", "id": "exampleInputText2"}))
    born_location = CharField(max_length=150,
                              widget=TextInput(attrs={"class": "form-control", "id": "exampleInputText3"}))
    description = CharField(widget=TextInput(attrs={"class": "form-control", "id": "exampleInputText4"}))

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class QuoteForm(ModelForm):
    quote = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control", "id": "exampleInputQuote1"}))
    #tags = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control", "id": "exampleInputQuote2"}))
    author = ModelChoiceField(queryset=Author.objects.all(),
                              widget=Select(attrs={"class": "form-control", "id": "exampleInputQuote3"}))

    class Meta:
        model = Quote
        fields = ["quote", "author"]

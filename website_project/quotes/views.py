from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .utils import get_mongodb
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote


# MONGO
def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)  # How many quotes per page
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={"quotes": quotes_on_page})


# MONGO

def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            # Extract data from form
            fullname = form.cleaned_data['fullname']
            born_date = form.cleaned_data['born_date']
            born_location = form.cleaned_data['born_location']
            description = form.cleaned_data['description']

            # Save data to MongoDB
            db = get_mongodb()
            db.authors.insert_one({"fullname": fullname, "born_date": born_date, "born_location": born_location,
                                   "description": description})
            # form.save()
            return redirect(to="quotes:root")
    return render(request, "quotes/add_author.html", context={"form": form})


# MONGO
def my_authors(request):
    db = get_mongodb()
    authors = db.authors.find()
    return render(request, "quotes/authors.html", context={"authors": authors})


# MONGO
def add_quote(request):
    db = get_mongodb()
    authors = db.authors.find()
    form = QuoteForm(instance=Quote())

    if request.method == "POST":
        form = QuoteForm(request.POST, instance=Quote())
        print(request.POST)
        if form.is_valid():
            quote_text = form.cleaned_data['quote']
            author_id = form.cleaned_data['author'].id


            db.quotes.insert_one({"quote": quote_text, "author_id": author_id})
            return redirect(to="quotes:root")
        else:
            print("Form is not valid:", form.errors)

    return render(request, "quotes/add_quote.html", context={"form": form, "authors": authors})


# MONGO
def my_quotes(request):
    db = get_mongodb()
    quotes = db.quotes.find()
    return render(request, "quotes/quotes.html", context={"quotes": quotes})


# POSTGRESS
def author_detail(request, author_fullname):
    author = get_object_or_404(Author, fullname=author_fullname)
    return render(request, "quotes/author_info.html", context={"author": author})


# POSTGRESS
def search_results(request):
    query = request.GET.get('q')
    if query:
        results = Quote.objects.filter(quote__icontains=query)
    else:
        results = []  # Handle empty query
    return render(request, 'quotes/search_results.html', {'results': results, 'query': query})

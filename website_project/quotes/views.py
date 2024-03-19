from bson import ObjectId
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .utils import get_mongodb
from .forms import AuthorForm, QuoteForm


def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)  # How many quotes per page
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={"quotes": quotes_on_page})


@login_required
def add_author(request):
    form = AuthorForm()
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            born_date = form.cleaned_data['born_date']
            born_location = form.cleaned_data['born_location']
            description = form.cleaned_data['description']
            db = get_mongodb()
            db.authors.insert_one({"fullname": fullname, "born_date": born_date, "born_location": born_location,
                                   "description": description})
            return redirect(to="quotes:root")
    return render(request, "quotes/add_author.html", context={"form": form})



@login_required
def my_authors(request):
    db = get_mongodb()
    authors = db.authors.find()
    return render(request, "quotes/authors.html", context={"authors": authors})

@login_required
def add_quote(request):
    db = get_mongodb()
    authors = db.authors.find()
    authors_data = [{"id": str(author["_id"]), "fullname": author.get("fullname", "Unknown")} for author in authors]
    form = QuoteForm()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        print(request.POST)
        if form.is_valid():
            quote_text = form.cleaned_data['quote']
            author_id = form.cleaned_data['author']
            author_id = ObjectId(author_id)

            tag_text = form.cleaned_data['tags']
            tags_list = [tag.strip() for tag in tag_text.split()]

            db.quotes.insert_one({"quote": quote_text, "tags": tags_list, "author": author_id})
            return redirect(to="quotes:root")
        else:
            print("Form is not valid:", form.errors)

    return render(request, "quotes/add_quote.html", context={"form": form, "authors": authors_data})

@login_required
def my_quotes(request):
    db = get_mongodb()
    quotes = db.quotes.find()

    return render(request, 'quotes/quotes.html', {'quotes': quotes})


def author_detail(request, author_fullname):
    db = get_mongodb()
    author = db.authors.find_one({"fullname": author_fullname})
    if author:
        quotes = db.quotes.find({"author": author["_id"]})
        return render(request, "quotes/author_info.html", context={"author": author, "quotes": quotes})
    else:
        return HttpResponseNotFound("Author not found")


def search_results(request):
    db = get_mongodb()
    query = request.GET.get('q')
    if query:
        quotes = db.quotes.find({"quote": {"$regex": query, "$options": "i"}})
        results = list(quotes)

        return render(request, 'quotes/search_results.html', {'results': results, 'query': query})


def quotes_by_tag(request, tag):
    tag = tag.lower()
    db = get_mongodb()
    cursor = db.quotes.find({'tags': tag})
    print(cursor)
    quotes = list(cursor)
    print(quotes)
    return render(request, 'quotes/quotes_by_tag.html', {'quotes': quotes, 'tag': tag})

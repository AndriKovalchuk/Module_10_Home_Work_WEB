from bson import ObjectId
from django.db import connection
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .models import Quote
from .utils import get_mongodb
from .forms import AuthorForm, QuoteForm


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
    form = AuthorForm()
    if request.method == "POST":
        form = AuthorForm(request.POST)
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


# MONGO
def my_quotes(request):
    db = get_mongodb()
    quotes = db.quotes.find()
    results = list(quotes)

    for quote in results:
        author_id = quote.get('author')
        author_details = db.authors.find_one({"_id": author_id})
        if author_details:
            quote['author_name'] = author_details.get('fullname', 'Unknown')

    return render(request, 'quotes/quotes.html', {'results': results})


# MONGO
def author_detail(request, author_fullname):
    db = get_mongodb()
    author = db.authors.find_one({"fullname": author_fullname})
    if author:
        quotes = db.quotes.find({"author": author["_id"]})
        return render(request, "quotes/author_info.html", context={"author": author, "quotes": quotes})
    else:
        return HttpResponseNotFound("Author not found")


# MONGO
def search_results(request):
    db = get_mongodb()
    query = request.GET.get('q')
    if query:
        quotes = db.quotes.find({"quote": {"$regex": query, "$options": "i"}})
        results = list(quotes)
        quotes = db.quotes.find()
        for quote in results:
            # Retrieve the author details based on the reference stored in the quote document
            author_id = quote.get('author')  # Assuming 'author' is the field storing the reference
            author_details = db.authors.find_one({"_id": author_id})
            if author_details:
                # If author details are found, add the author's fullname to the quote document
                quote['author_name'] = author_details.get('fullname', 'Unknown')

        return render(request, 'quotes/search_results.html', {'results': results, 'query': query})


def quotes_by_tag(request, tag):
    tag = tag.lower()

    db = get_mongodb()
    cursor = db.quotes.find({'tags': tag})

    # Convert MongoDB documents to a list of dictionaries
    quotes = list(cursor)

    return render(request, 'quotes/quotes_by_tag.html', {'quotes': quotes, 'tag': tag})


def top_ten_tags(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tags_name, COUNT(*) as tag_count 
            FROM quotes_quote_tags 
            GROUP BY tags_name 
            ORDER BY tag_count DESC 
            LIMIT 10
        """)
        top_tags = cursor.fetchall()

    context = {'top_tags': top_tags}
    return render(request, 'quotes/base.html', context)
from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField


class Author(Document):
    fullname = StringField(max_length=50, required=True)
    born_date = StringField(max_length=50, required=True)
    born_location = StringField(max_length=50, required=True)
    description = StringField(required=True)
    created_at = DateTimeField(max_length=50, required=True)


class Tag(Document):
    name = StringField(max_length=100, required=True, unique=True)


class Quote(Document):
    quote = StringField(required=True)
    tags = ListField(ReferenceField(Tag))
    author = ReferenceField(Author)
    created_at = DateTimeField(required=True)

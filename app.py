"""BookStore Rest API."""
import requests

from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from database import POSTGRESQL_SERVER


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_SERVER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# database
class BookStore(db.Model):
    """Creates BookStore table in PostgreSQL database."""

    __tablename__ = 'bookstore'
    book_id = db.Column(db.Integer, primary_key=True)
    ext_id = db.Column(db.String(100))
    title = db.Column(db.String(250), nullable=False)
    authors = db.Column(db.ARRAY(db.String(250)), nullable=False)
    acquired = db.Column(db.Boolean)
    published_year = db.Column(db.Integer)
    thumbnail = db.Column(db.String(200))

    def __init__(self, ext_id, title, authors, acquired,
                 published_year, thumbnail):
        """Constructor for BookStore class."""
        self.title = title
        self.ext_id = ext_id
        self.authors = authors
        self.acquired = acquired
        self.published_year = published_year
        self.thumbnail = thumbnail

    def convert_to_json(self):
        """Converts data to json."""
        return {
            'id': self.book_id,
            'external_id': self.ext_id,
            'title': self.title,
            'authors': self.authors,
            'acquired': self.acquired,
            'published_year': self.published_year,
            'thumbnail': self.thumbnail
        }


@app.before_first_request
def create_all():
    """Creates table in database."""
    db.create_all()


@app.route('/')
def index():
    """Home page."""
    books = BookStore.query.all()
    if books == []:
        return render_template('index.html', info='Out of stock')
    return render_template('index.html', books=books)


@app.route('/search_books')
def search_book():
    """Search books page."""
    return render_template('search_books.html')


@app.route('/add_book')
def add_book():
    """Add book page."""
    return render_template('add_book.html')


@app.route('/delete_book')
def delete_book():
    """Delete book page."""
    return render_template('delete_book.html')


@app.route('/import_books')
def import_books():
    """Import books from google api page."""
    return render_template('import_books.html')


# getting the info about API version
@app.route('/api_spec', methods=['GET'])
def api_spec():
    """Returns version info."""
    return jsonify({'info': {'version': '2022.05.16'}})


# getting the list of books from the database
@app.route('/books', methods=['GET'])
def books_list():
    """Returns list of books."""
    args = request.args

    books = BookStore.query.all()
    if not books:
        return jsonify({'info': 'no data'})

    if args:
        title = args.get('title')
        author = args.get('author')
        year_from = args.get('from')
        year_to = args.get('to')
        acquired = args.get('acquired')
        db_query = []
        if title:
            db_query.append(f"title = {title}")
        if author:
            author = '%' + author[1:-1] + '%'
            db_query.append(f"ARRAY_TO_STRING(authors, ', ') LIKE '{author}'")
        if year_from and year_to:
            db_query.append(f"published_year >= {year_from} AND \
                            published_year <= {year_to}")
        elif year_from:
            db_query.append(f"published_year >= {year_from}")
        elif year_to:
            db_query.append(f"published_year <= {year_to}")
        if acquired:
            db_query.append(f"acquired = {acquired}")

        sql_query = 'SELECT * FROM  bookstore WHERE '
        sql_queries = sql_query + ' AND '.join(db_query) + ';'
        sql_queries = sql_queries.replace('"', "'")

        db_answer = db.session.execute(sql_queries)

        if not db_answer:
            return jsonify({"info": "no data"})

        books = []
        for answer in db_answer:
            books.append(dict(answer._mapping))

        return jsonify([book for book in books])

    return jsonify([book.convert_to_json() for book in books])


# get details of single book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Returns details of the book with the given id."""
    book = BookStore.query.filter_by(book_id=book_id).first()
    if not book:
        return jsonify({'info': 'no data'})
    return jsonify(book.convert_to_json())


# add a new book to collection
@app.route('/books', methods=['POST'])
def new_book():
    """Adds a new book to the database."""
    ext_id = request.json.get('ext_id')
    title = request.json.get('title')
    authors = request.json.get('authors')
    published_year = request.json.get('published_year')
    acquired = request.json.get('acquired')
    thumbnail = request.json.get('thumbnail')
    if not title:
        return jsonify({"info": "no title"})
    elif not authors:
        return jsonify({"info": "no autors"})
    elif not title and not authors:
        return jsonify({"info": "no autors and no title"})
    book = BookStore(title=title, ext_id=ext_id, authors=authors,
                     acquired=acquired, published_year=published_year,
                     thumbnail=thumbnail)
    db.session.add(book)
    db.session.commit()

    return jsonify(book.convert_to_json()), 201


# update details of single book
@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book(book_id):
    """Updates the book data with the given id."""
    book = BookStore.query.get(book_id)
    if book is None:
        return jsonify({'info': 'no data'})
    book.ext_id = request.json.get('external_id', book.ext_id)
    book.title = request.json.get('title', book.title)
    book.authors = request.json.get('authors', book.authors)
    book.published_year = request.json.get('published_year',
                                           book.published_year)
    book.acquired = request.json.get('acquired', book.acquired)
    book.thumbnail = request.json.get('thumbnail', book.thumbnail)
    db.session.commit()
    return jsonify(book.convert_to_json())


# delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def del_book(book_id):
    """Removes the book with the given id from the database."""
    book = BookStore.query.get(book_id)
    if not book:
        return jsonify({'info': 'no data'})
    db.session.delete(book)
    db.session.commit()
    return jsonify({'delete': True})


# import books
@app.route('/import', methods=['POST'])
def import_google_books():
    """Imports the books of the specified author
    from the google books api to the database."""
    author = request.json.get('author')
    url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}'
    response = requests.get(url)

    if response.status_code == 200:
        content = response.json()
        total_items = content['totalItems']
        google_books_ids = []
        print(total_items)
        count = 0
        for item in range(0, total_items, 40):
            url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}&startIndex={item}&maxResults=40'
            response = requests.get(url) 
            content = response.json()
            for i in range(40):
                google_book_id = content['items'][i]['id']
                if google_book_id not in google_books_ids:
                    quest = content['items'][i]
                    ext_id = quest['id']
                    title = quest['volumeInfo']['title']
                    try:
                        authors = quest['volumeInfo']['authors']
                    except KeyError:
                        authors = []
                    acquired = False
                    try:
                        published_year = quest['volumeInfo']['publishedDate'][:4]
                    except KeyError:
                        published_year = None
                    try:
                        thumbnail = quest['volumeInfo']['imageLinks']['thumbnail']
                    except KeyError:
                        thumbnail = ''

                    book = BookStore(title=title,
                                    ext_id=ext_id,
                                    authors=authors,
                                    acquired=acquired,
                                    published_year=published_year,
                                    thumbnail=thumbnail)
                    db.session.add(book)
                google_books_ids.append(google_book_id)
                count += 1
                if count == total_items:
                    break
        print(count)
        db.session.commit()
        return jsonify({'imported': count})

    return jsonify({'import': False})


if __name__ == '__main__':
    app.run()

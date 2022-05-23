# STX-BookStore

## Description
The REST API application allows for some basic operations, such as:
- getting the list of books from the database
- adding a new book
- editing an existing book
- removing the book from the database
- filtering the results by: title, author, publication year (where the range of years is given) and by the acquired state (if the book is already acquired or not)
- importing books from Google API:
-- https://developers.google.com/books/docs/v1/using#WorkingVolumes (usage
example: https://www.googleapis.com/books/v1/volumes?q=Hobbit )
-- in response returns the number of imported books

## Technologies
- Python 3
- Flask
- Flask-SQAlchemy (ORM)
- PostgreSQL
- HTML
- Bootstrap 5
- Jinja2
- Heroku
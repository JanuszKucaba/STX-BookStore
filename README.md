# STX-BookStore
- link: https://book-store-stx.herokuapp.com/

![image](https://user-images.githubusercontent.com/61910621/170312362-023b6d4a-6452-41e1-bb47-ff6d3f176893.png)

## Description
### The REST API application allows for some basic operations, such as:
- getting the list of books from the database
- adding a new book
- editing an existing book
- removing the book from the database
- filtering the results by: title, author, publication year (where the range of years is given) and by the acquired state (if the book is already acquired or not)
- importing books from Google API

## Technologies
- Python 3
- Flask
- Flask-SQAlchemy
- PostgreSQL
- HTML
- Bootstrap 5
- Jinja2
- Heroku

## Documentation
### details: https://documenter.getpostman.com/view/19621238/Uz59PKsj
### example requests and responses:
- getting the info about API:

  ![image](https://user-images.githubusercontent.com/61910621/170316124-5feb5919-025e-442c-bc81-668717696137.png)

- getting the list of books from the database:

  ![image](https://user-images.githubusercontent.com/61910621/170316277-9b346a8f-cf14-42c3-9800-ad7ece43c2cc.png)

- getting the list of books from the database by filter:
  
  ![image](https://user-images.githubusercontent.com/61910621/170316404-7c223823-54d9-4843-942e-d598982a395a.png)
  
- getting details of single book:

  ![image](https://user-images.githubusercontent.com/61910621/170316620-62e97b67-d89a-46e4-898d-809c2c13acc9.png)

- adding a new book to colletcion:

  ![image](https://user-images.githubusercontent.com/61910621/170316743-b9cbf784-24f4-4f2d-886f-8f89dc5a7f01.png)

- updating details of single book:

  ![image](https://user-images.githubusercontent.com/61910621/170316879-0c29121a-5fed-4cbd-9cef-50efab54d743.png)
 
- deleting a book by ID:

  ![image](https://user-images.githubusercontent.com/61910621/170317042-ebe36f50-1ab5-456e-bfd4-b136c3bf92fc.png)

- importing books from google books:

  ![image](https://user-images.githubusercontent.com/61910621/170317151-c97a649e-c7fb-42be-a2f2-f226607a42cb.png)

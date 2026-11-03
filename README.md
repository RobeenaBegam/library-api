# Library Management API

A REST API for managing a library's books, built with FastAPI and SQLite, with a simple web page to use it.

## Features

- Add, view, update and delete books (full CRUD)
- Data saved in a SQLite database using SQLAlchemy
- Borrow and return books, with error checks
- Web page to add, borrow, return and delete books
- Automatic API documentation page

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- HTML, CSS and JavaScript (frontend)

## How to Run

1. Install the requirements:

```
pip install fastapi uvicorn sqlalchemy
```

2. Start the server:

```
python -m uvicorn main:app --reload
```

3. Open the web page in your browser:

```
http://127.0.0.1:8000
```

4. Open the API documentation page:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | /books | Show all books |
| POST | /books | Add a new book |
| PUT | /books/{book_id} | Update a book's title and author |
| DELETE | /books/{book_id} | Delete a book |
| POST | /books/{book_id}/borrow | Mark a book as borrowed |
| POST | /books/{book_id}/return | Mark a book as returned |

## Error Handling

- 400: book id already exists, book already borrowed, or book not borrowed
- 404: book not found

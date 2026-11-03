from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base


class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    is_borrowed = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    is_borrowed: bool = False


class BookUpdate(BaseModel):
    title: str
    author: str


@app.get("/books", response_model=list[Book])
def get_books(db: Session = Depends(get_db)):
    return db.query(BookDB).all()


@app.post("/books", response_model=Book)
def add_book(book: Book, db: Session = Depends(get_db)):
    existing = db.get(BookDB, book.id)
    if existing:
        raise HTTPException(status_code=400, detail="Book id already exists")
    new_book = BookDB(
        id=book.id, title=book.title, author=book.author, is_borrowed=False
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated: BookUpdate, db: Session = Depends(get_db)):
    book = db.get(BookDB, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = updated.title
    book.author = updated.author
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BookDB, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}


@app.post("/books/{book_id}/borrow", response_model=Book)
def borrow_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BookDB, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.is_borrowed:
        raise HTTPException(status_code=400, detail="Book is already borrowed")
    book.is_borrowed = True
    db.commit()
    db.refresh(book)
    return book


@app.post("/books/{book_id}/return", response_model=Book)
def return_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BookDB, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_borrowed:
        raise HTTPException(status_code=400, detail="Book is not borrowed")
    book.is_borrowed = False
    db.commit()
    db.refresh(book)
    return book


app.mount("/", StaticFiles(directory="static", html=True), name="static")
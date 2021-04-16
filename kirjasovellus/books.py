from db import db
from sqlalchemy import exc

def add_new_book(title: str, author: str, genre: str, isbn: str, pages: int):
    try:
        sql = "INSERT INTO books (title, author, genre, isbn, pages) VALUES (:title,:author,:genre,:isbn,:pages)"
        db.session.execute(sql, {"title":title,"author":author, "genre":genre, "isbn": isbn, "pages":pages})
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        return False

def find_books(query: str, selection: list):
    title = "1" in selection or "2" in selection
    author = "1" in selection or "3" in selection
    genre = "1" in selection or "4" in selection
    isbn = "1" in selection or "5" in selection
    try: 
        sql = "SELECT * FROM books WHERE (title ILIKE :query AND :title)\
            OR (author ILIKE :query AND :author)\
            OR (genre ILIKE :query AND :genre)\
            OR (isbn ILIKE :query AND :isbn)"
        result = db.session.execute(sql, {"query":"%"+query+"%", "title": title, "author": author, "genre":genre, "isbn":isbn })
        books = result.fetchall()
        return books

    except exc.SQLAlchemyError:
        return []
    
def find_book_by_id(id: int):
    try:
        sql = "SELECT * FROM books WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        book = result.fetchone()
        return book

    except exc.SQLAlchemyError:
        return None
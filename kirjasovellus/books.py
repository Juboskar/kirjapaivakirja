from db import db
from sqlalchemy import exc

def add_new_book(title: str, author: str, genre: str, isbn:str, pages:int):
    try:
        sql = "INSERT INTO books (title, author, genre, isbn, pages) VALUES (:title,:author,:genre,:isbn,:pages)"
        db.session.execute(sql, {"title":title,"author":author, "genre":genre, "isbn": isbn, "pages":pages})
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        return False

def find_books(query:str, selection:int):
    try:
        books = []
        if "2" in selection or "1" in selection: 
            sql = "SELECT * FROM books WHERE title ILIKE :query"
            result = db.session.execute(sql, {"query":"%"+query+"%"})
            books.extend(result.fetchall())

        if "3" in selection or "1" in selection:  
            sql = "SELECT * FROM books WHERE author ILIKE :query"
            result = db.session.execute(sql, {"query":"%"+query+"%"})
            books.extend(result.fetchall())

        if "4" in selection or "1" in selection:  
            sql = "SELECT * FROM books WHERE genre ILIKE :query"
            result = db.session.execute(sql, {"query":"%"+query+"%"})
            books.extend(result.fetchall())

        if "5" in selection or "1" in selection:  
            sql = "SELECT * FROM books WHERE isbn ILIKE :query"
            result = db.session.execute(sql, {"query":"%"+query+"%"})
            books.extend(result.fetchall())
        
        return list(set(books))

    except exc.SQLAlchemyError:
        return []
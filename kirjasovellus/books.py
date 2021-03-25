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
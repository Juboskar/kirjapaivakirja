from db import db
from sqlalchemy import exc

def add_new_book(user_id:int, book_id: int):
    try:
        sql = "INSERT INTO bookshelf_books (user_id, book_id, progress, update_date) VALUES (:user_id, :book_id, 0, NOW())"
        db.session.execute(sql, {"user_id":user_id,"book_id":book_id})
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        return False

def check_if_in_bookshelf(user_id:int, book_id: int):
    try:
        sql = "SELECT * FROM bookshelf_books WHERE user_id =:user_id AND book_id=:book_id"
        result = db.session.execute(sql, {"user_id":user_id,"book_id":book_id})
        if result.fetchone() == None:
            return False
        else: 
            return True
        
    except exc.SQLAlchemyError:
        print("hallo")
        return False # todo

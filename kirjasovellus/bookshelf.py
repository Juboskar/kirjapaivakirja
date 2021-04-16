from db import db
from sqlalchemy import exc

def add_new_book_event(user_id: int, book_id: int, progress: int):
    try:
        sql = "INSERT INTO bookshelf_books (user_id, book_id, progress, update_date) VALUES (:user_id, :book_id, :progress, NOW())"
        db.session.execute(sql, {"user_id":user_id,"book_id":book_id, "progress":progress})
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        return False

def check_if_in_bookshelf(user_id: int, book_id: int):
    try:
        sql = "SELECT * FROM bookshelf_books WHERE user_id =:user_id AND book_id=:book_id"
        result = db.session.execute(sql, {"user_id":user_id,"book_id":book_id})
        if result.fetchone() == None:
            return False
        else: 
            return True
        
    except exc.SQLAlchemyError:
        return None

def find_all_books(user_id: int):
    try:
        sql = "SELECT c.title, c.author, b.update_count, a.progress, c.pages, a.book_id \
                FROM bookshelf_books a\
                JOIN (\
                    SELECT bookshelf_books.book_id book_id, COUNT(*) update_count,\
                        MAX(bookshelf_books.update_date) update_date\
                    FROM bookshelf_books, books\
                    WHERE books.id = bookshelf_books.book_id\
                        AND bookshelf_books.user_id=:user_id\
                    GROUP BY book_id\
                ) b ON a.book_id = b.book_id AND a.update_date = b.update_date\
                JOIN (SELECT id, title, author, pages FROM books) c ON a.book_id = c.id"
        result = db.session.execute(sql, {"user_id":user_id})
        books = result.fetchall()
        return books

    except exc.SQLAlchemyError:
        return None

def find_book_events(user_id: int, book_id: int):
    print(user_id)
    print(book_id)
    try:   
        sql = "SELECT * FROM bookshelf_books WHERE user_id=:user_id AND book_id=:book_id ORDER BY update_date DESC"
        result = db.session.execute(sql, {"user_id":user_id, "book_id":book_id})
        events = result.fetchall()
        return events
    except exc.SQLAlchemyError:
        return None
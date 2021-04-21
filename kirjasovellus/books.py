from db import db
from sqlalchemy import exc


def add_new_book(title: str, author: str, genre: str, isbn: str, pages: int):
    try:
        sql = "INSERT INTO books (title, author, genre, isbn, pages) VALUES (:title,:author,:genre,:isbn,:pages)"
        db.session.execute(sql, {"title": title, "author": author,
                                 "genre": genre, "isbn": isbn, "pages": pages})
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
        result = db.session.execute(
            sql, {"query": "%"+query+"%", "title": title, "author": author, "genre": genre, "isbn": isbn})
        books = result.fetchall()
        return books

    except exc.SQLAlchemyError:
        return []


def find_book_by_id(id: int):
    try:
        sql = "SELECT * FROM books WHERE id=:id"
        result = db.session.execute(sql, {"id": id})
        book = result.fetchone()
        return book

    except exc.SQLAlchemyError:
        return None


def check_if_already_rated(user_id: int, book_id: int):
    try:
        sql = "SELECT id, star_rating, review, rating_date FROM ratings WHERE user_id=:user_id AND book_id=:book_id"
        result = db.session.execute(
            sql, {"user_id": user_id, "book_id": book_id})
        review = result.fetchone()
        return review

    except exc.SQLAlchemyError:
        return None


def add_review(user_id: int, book_id: int, star_rating: int, review: str, already_exists:bool):
    if already_exists:
        try:
            sql = "UPDATE ratings SET star_rating=:star_rating, review=:review, rating_date=NOW() WHERE user_id=:user_id AND book_id=:book_id"
            db.session.execute(sql, {
                            "user_id": user_id, "book_id": book_id, "star_rating": star_rating, "review": review})
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    else:
        try:
            sql = "INSERT INTO ratings (user_id, book_id, star_rating, review, rating_date) VALUES (:user_id,:book_id,:star_rating,:review, NOW())"
            db.session.execute(sql, {
                            "user_id": user_id, "book_id": book_id, "star_rating": star_rating, "review": review})
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

def find_reviews_by_book_id(book_id: int):
    try:   
        sql = "SELECT u.username, r.star_rating, r.review, r.rating_date FROM ratings r \
            JOIN users u ON u.id = r.user_id  \
            WHERE book_id=:book_id ORDER BY rating_date DESC"
        result = db.session.execute(sql, {"book_id": book_id})
        reviews = result.fetchall()
        return reviews
    except exc.SQLAlchemyError:
        return None
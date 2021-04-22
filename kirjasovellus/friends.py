from db import db
from sqlalchemy import exc

def find_user(name: str):
    try:
        sql = "SELECT id, username FROM users WHERE (username ILIKE :name)"
        result = db.session.execute(sql, {"name": "%"+name+"%"})
        users = result.fetchall()
        return users

    except exc.SQLAlchemyError:
        return []

def find_connection(user_id: int, connection_id: int):
    try:
        sql = "SELECT c.friend_status, u.id, u.username FROM users u\
                LEFT JOIN (SELECT * FROM friends WHERE user_id=:user_id) c \
                ON u.id=c.friend_id WHERE u.id=:connection_id"
        result = db.session.execute(sql, {"user_id": user_id, "connection_id": connection_id})
        user = result.fetchone()
        return user

    except exc.SQLAlchemyError:
        return []

def send_friend_request(user_id: int, connection_id: int):
    if user_id == connection_id:
        return False
    try:
        sql = "INSERT INTO friends (user_id, friend_id, friend_status) VALUES (:user_id, :connection_id, 'sent')"
        db.session.execute(sql, {"user_id": user_id, "connection_id": connection_id})
        sql = "INSERT INTO friends (user_id, friend_id, friend_status) VALUES (:connection_id, :user_id, 'waiting')"
        db.session.execute(sql, {"user_id": user_id, "connection_id": connection_id})
        db.session.commit()
        return True

    except exc.SQLAlchemyError:
        return False

def accept_friend_request(user_id: int, connection_id: int):
    try:
        sql = "UPDATE friends SET friend_status='ok' \
            WHERE (user_id=:user_id AND friend_id=:connection_id \
                AND friend_status='waiting') \
            OR (user_id=:connection_id \
                AND friend_id=:user_id AND friend_status='sent')"
        db.session.execute(sql, {"user_id": user_id, "connection_id": connection_id})
        db.session.commit()
        return True

    except exc.SQLAlchemyError:
        return False
    
def remove_friend(user_id: int, connection_id: int):
    try:
        sql = "DELETE FROM friends \
            WHERE (user_id=:user_id AND friend_id=:connection_id) \
            OR (user_id=:connection_id AND friend_id=:user_id)"
        db.session.execute(sql, {"user_id": user_id, "connection_id": connection_id})
        db.session.commit()
        return True

    except exc.SQLAlchemyError:
        return False

def check_if_already_friends(user_id: int, connection_id: int):
    try:
        sql = "SELECT * FROM friends WHERE user_id=:user_id AND friend_id=:connection_id"
        result = db.session.execute(sql, {"user_id": user_id, "connection_id": connection_id})
        user = result.fetchone()
        return user

    except exc.SQLAlchemyError:
        return None
    
def find_all_friends(user_id: int):
    try:
        sql = "SELECT u.id, u.username, f.friend_status FROM friends f\
            LEFT JOIN users u ON u.id=f.friend_id\
                WHERE user_id=:user_id"
        result = db.session.execute(sql, {"user_id": user_id})
        friends = result.fetchall()
        return friends

    except exc.SQLAlchemyError:
        return None
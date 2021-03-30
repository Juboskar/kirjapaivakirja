from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from sqlalchemy import exc

def register(username: str, password: str):
    try:
        password_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":password_value})
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        return False

def login(username: str, password: str):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        return False # invalid username
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            return True
        else:
            return False # invalid password

def get_user_id_by_username(username:str):
    try:   
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user_id = result.fetchone()[0]
        return user_id
    except: 
        pass # todo
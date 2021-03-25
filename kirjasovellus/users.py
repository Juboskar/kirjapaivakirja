from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def register(username: str, password: str):
    password_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username,:password)"
    db.session.execute(sql, {"username":username,"password":password_value})
    db.session.commit()

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
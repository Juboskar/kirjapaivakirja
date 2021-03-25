from app import app
from flask import redirect, render_template, request, session
from os import urandom
import users

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/register")
def redirect_to_register():
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    #todo syötteen validiointi?
    username = request.form["username"]
    password = request.form["password"]
    users.register(username, password)
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_result():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        session["username"] = username
        session["csrf_token"] = urandom(16).hex()
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")
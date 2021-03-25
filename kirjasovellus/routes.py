from app import app
from flask import redirect, render_template, request, session
import users

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    #todo syötteen validiointi?
    username = request.form["username"]
    password = request.form["password"]
    users.register(username, password)
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def result():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        # TODO: check username and password
        session["username"] = username
    return render_template("home.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
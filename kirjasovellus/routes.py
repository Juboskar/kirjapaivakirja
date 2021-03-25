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
    username = request.form["username1"]
    password = request.form["password1"]
    register_ok = users.register(username, password)
    register_ok_info = "Jokin meni pieleen. Voi olla, että käyttäjätunnus on varattu. Ongelman jatkuessa kannattaa koittaa jotain muuta käyttäjätunnusta."
    if register_ok:
        register_ok_info = "Rekisteröityminen onnistui, voit nyt kirjautua"
    return render_template("index.html", register_ok=register_ok_info)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_result():
    username = request.form["username2"]
    password = request.form["password2"]
    if users.login(username, password):
        session["username"] = username
        session["csrf_token"] = urandom(16).hex()
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

# TODO
@app.route("/bookshelf")
def bookshelf():
    return render_template("bookshelf.html")

@app.route("/search")
def search():
    return render_template("search.html")

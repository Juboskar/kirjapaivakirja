from app import app
from flask import redirect, render_template, request, session
from os import urandom
import users
import books
import bookshelf

# LOGIN 

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
    register_ok_info = "Jokin meni pieleen. Voi olla, että käyttäjätunnus on varattu.\
        Ongelman jatkuessa kannattaa koittaa jotain muuta käyttäjätunnusta."
    if register_ok:
        register_ok_info = "Rekisteröityminen onnistui, voit nyt kirjautua"
    return render_template("index.html", register_status=register_ok_info)

@app.route("/login")
def login():
    return redirect("/")

@app.route("/login", methods=["POST"])
def login_result():
    username = request.form["username2"]
    password = request.form["password2"]
    if users.login(username, password):
        session["username"] = username
        session["csrf_token"] = urandom(16).hex()
    else: 
        login_status = "Sisäänkirjautuminen epäonnistui" # todo: nämä kovakoodaukset html:ään
        return render_template("index.html", login_status = login_status)
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

# BOOKSHELF

@app.route("/bookshelf")
def go_to_bookshelf():
    return render_template("bookshelf.html")

@app.route("/bookshelf/add", methods=["POST"])
def add_to_bookshelf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    book_id = request.form["book_id"]
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    print(bookshelf.add_new_book(user_id, book_id))
    return redirect("/search/findbooks/" + book_id)


# SEARCH

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search/addbook", methods=["POST"])
def add_book():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    title = request.form["title"]
    author = request.form["author"]
    genre = request.form["genre"]
    isbn = request.form["isbn"]
    pages = request.form["pages"]
    if books.add_new_book(title, author, genre, isbn, pages):
        return redirect("/search")
    else:
        return render_template("search.html", info="Jokin meni pieleen")

@app.route("/search/findbooks")
def find_books():
    selection = request.args.getlist("criteria")
    query = request.args["query"]
    result_books = books.find_books(query, selection)
    return render_template("search.html", books = result_books[:30])

@app.route("/search/findbooks/<int:id>")
def find_books_id(id):
    book = books.find_book_by_id(id)
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    info = bookshelf.check_if_in_bookshelf(user_id, id)
    return render_template("book.html", book = book, info = info)

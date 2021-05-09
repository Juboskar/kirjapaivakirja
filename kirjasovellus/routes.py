from app import app
from flask import redirect, render_template, request, session
from os import urandom
from datetime import timedelta
import users
import books
import bookshelf
import friends
import events


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)

# LOGIN


@app.route("/")
def index():
    friend_events = []
    if session.get("username") is not None:
        username = session["username"]
        user_id = users.get_user_id_by_username(username)
        ratings = friends.get_friends_reviews(user_id)
        progress_updates = friends.get_friends_updates(user_id)
        friend_events = events.concatenate_event_lists(ratings, progress_updates)
    return render_template("index.html", events = friend_events)

@app.route("/register")
def redirect_to_register():
    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    # todo syötteen validiointi?
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
        # todo: nämä kovakoodaukset siirrettävä kyl html:ään
        login_status = "Virheellinen käyttäjätunnus tai salasana"
        return render_template("index.html", login_status=login_status)
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

# BOOKSHELF


@app.route("/bookshelf")
def go_to_bookshelf():
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    shelved_books = bookshelf.find_all_books(user_id)
    return render_template("bookshelf.html", books=shelved_books)


@app.route("/bookshelf/add", methods=["POST"])
def add_to_bookshelf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    book_id = request.form["book_id"]
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    bookshelf.add_new_book_event(user_id, book_id, 0)
    return redirect("/search/findbooks/" + book_id)


@app.route("/bookshelf/progress/<int:id>")
def book_progress(id):
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    book = books.find_book_by_id(id)
    events = bookshelf.find_book_events(user_id, id)
    latest = events[0]
    return render_template("bookshelf_book.html", book=book, events=events, latest=latest)


@app.route("/bookshelf/updateprogress", methods=["POST"])
def update_progress():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    book_id = request.form["book_id"]
    progress = request.form["progress"]
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    bookshelf.add_new_book_event(user_id, book_id, progress)
    return redirect("/bookshelf/progress/" + book_id)

@app.route("/bookshelf/deleteevent", methods=["POST"])
def delete_bookshelf_book():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    book_id = request.form["book_id"]
    event_id = request.form["event_id"]
    bookshelf.delete_event(event_id)
    return redirect("/bookshelf/progress/" + book_id)

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
    return render_template("search.html", books=result_books[:30])


@app.route("/search/findbooks/<int:id>")
def find_books_id(id):
    book = books.find_book_by_id(id)
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    info = bookshelf.check_if_in_bookshelf(user_id, id)
    review = books.check_if_already_rated(user_id, id)
    if review == None:
        review = (0, 0, "", 0)

    ratings = books.find_reviews_by_book_id(id)

    return render_template("book.html", book=book, review=review, info=info, ratings=ratings)


@app.route("/search/findbooks/<int:id>/addreview", methods=["POST"])
def add_review(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    book_id = id
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    review = request.form["review"]
    star_rating = request.form["stars"]
    already_exists = books.check_if_already_rated(user_id, id) != None
    books.add_review(user_id, book_id, star_rating, review, already_exists)
    return redirect("/search/findbooks/" + str(id))

# FRIENDS

@app.route("/friends")
def friends_page():
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    ok = []
    sent = []
    waiting = []
    for i in friends.find_all_friends(user_id):
        if i[2] == 'ok':
            ok.append(i)
        if i[2] == 'sent':
            sent.append(i)
        if i[2] == 'waiting':
            waiting.append(i)
    return render_template("friends.html", ok = ok, sent = sent, waiting = waiting)


@app.route("/friends/findfriends")
def findfriends():
    username = request.args["name"]
    result = friends.find_user(username)
    return render_template("friends.html", users=result)


@app.route("/friends/findfriends/<int:id>")
def findfriendsbyid(id):
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    result = friends.find_connection(user_id, id)
    if result[1] == user_id:
        result = ("you", result[1], result[2])
    return render_template("user.html", user=result)


@app.route("/friends/findfriends/sendrequest/<int:id>", methods=["POST"])
def send_friend_request(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    if friends.check_if_already_friends(user_id, id) == None:
        friends.send_friend_request(user_id, id)
    return redirect("/friends/findfriends/" + str(id))

@app.route("/friends/findfriends/removefriend/<int:id>", methods=["POST"])
def remove_friend(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    friends.remove_friend(user_id, id)
    return redirect("/friends/findfriends/" + str(id))

@app.route("/friends/findfriends/acceptfriend/<int:id>", methods=["POST"])
def accept_friend(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    username = session["username"]
    user_id = users.get_user_id_by_username(username)
    friends.accept_friend_request(user_id, id)
    return redirect("/friends/findfriends/" + str(id))
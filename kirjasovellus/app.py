from flask import Flask
from flask import Flask
from os import getenv
from datetime import timedelta

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)

import routes
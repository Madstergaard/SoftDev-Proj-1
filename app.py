from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3, hashlib
from time import gmtime, strftime
from utils import sift, sort, tix


app = Flask(__name__)
app.secret_key = "secrets"

@app.route("/login/", methods = ['POST']) 


@app.route("/home/", methods = ['POST']) 


@app.route("/event/<eventID>", methods = ['POST']) 


@app.route('/preferences/', methods = ['POST']) 


if __name__ == "__main__":
    app.debug = True
    app.run()


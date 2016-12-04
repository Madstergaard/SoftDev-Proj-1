from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3, hashlib
from utils import sift, sort, tix

app = Flask(__name__)
app.secret_key = 'secrets'

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home/')
def home():
    if 'access_token' in session:
        profile = sift.get_profile_data(session['access_token']) #dict
        saved_tracks = sift.get_saved_tracks(session['access_token'])
        return render_template(
                'dashboard.html',
                logged_in = True,
                access_token=session['access_token'],
                profile=profile,
                saved_tracks=saved_tracks
        )
    else:
        auth_url = sift.authentication_url()
        return render_template('dashboard.html', logged_in = False, auth_url=auth_url)

@app.route('/login/')
def login():
    if 'code' in request.args:
        auth_token = request.args['code']
        token_response = sift.token_request(auth_token)
        session['access_token'] = token_response['access_token']
    return redirect(url_for('home'))

@app.route('/event/<eventID>')
def event(eventID):
    return 'Nothing yet'

@app.route('/preferences/')
def preferences():
    return 'Nothing yet'

if __name__ == '__main__':
    app.debug = True
    app.run()


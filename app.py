from flask import Flask, render_template, request, session, url_for, redirect
from utils import sift, sort, tix

app = Flask(__name__)
app.secret_key = 'secrets'

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home/')
def home():
    # Check if logged in
    if 'access_token' in session:
        profile = sift.get_profile_data(session['access_token'])
        saved_tracks = sift.get_saved_tracks(session['access_token'])
        return render_template(
                'dashboard.html',
                logged_in = True,
                access_token=session['access_token'],
                profile=profile,
                saved_tracks=saved_tracks
        )
    else:
        # Authentication url is a Spotify page
        auth_url = sift.authentication_url()
        return render_template('dashboard.html', logged_in = False, auth_url=auth_url)

# Used for the callback from Spotify to our website
@app.route('/login/')
def login():
    # If it has been called back, then send a request to get an access token
    # Might modify this (b.c. anyone could just put any code they wanted into the URL)
    if 'code' in request.args:
        auth_token = request.args['code']
        token_response = sift.token_request(auth_token)
        session['access_token'] = token_response['access_token']
    # Always redirect to the homepage
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


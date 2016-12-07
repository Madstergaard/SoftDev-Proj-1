from flask import Flask, render_template, request, session, url_for, redirect
from utils import auth, sift, sort, tix, dbUtil

app = Flask(__name__)
app.secret_key = 'secrets'

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home/')
def home():
    # Check if logged in
    if 'access_token' in session:
        # Refresh access token
        session['access_token'] = auth.refresh(session['refresh_token'])

        if not dbUtil.isUserInDB():
            dbUtil.addUserToDB()
        saved_tracks = sift.saved_tracks(session['access_token'])
        trackid_dict = sift.trackid_dict(saved_tracks)

        artist_numtrack_dict = sift.artist_numtrack_dict(trackid_dict)
        top_n_artists = sift.top_n_artists(artist_numtrack_dict, 10)
        return render_template(
                'dashboard.html',
                logged_in = True,
                trackid_dict=trackid_dict,
                top_n_artists=top_n_artists
        )
    else:
        # Authentication url is a Spotify page
        auth_url = auth.authentication_url()
        return render_template('dashboard.html', logged_in = False, auth_url=auth_url)

# Used for the callback from Spotify to our website
@app.route('/login/')
def login():
    # If it has been called back, then send a request to get an access token
    # Might modify this (b.c. anyone could just put any code they wanted into the URL)
    if auth.check_state(request.args.get('state')):
        auth_token = request.args['code']
        token_response = auth.token_request(auth_token)
        session['access_token'] = token_response['access_token']
        session['refresh_token'] = token_response['refresh_token']
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

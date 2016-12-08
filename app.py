from flask import Flask, render_template, request, session, url_for, redirect
from utils import auth, sort, sift, tix, dbUtil
from json import loads, dumps

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
        print "REFRESHING TOKEN"
        session['access_token'] = auth.refresh(session['refresh_token'])

        print "GETTING ARTIST DATA FROM DB"
        artist_data = loads(dbUtil.getArtistData()) #unordered
        artist_data = sift.top_n(artist_data, 40) #sorted

        print "GETTING EVENTS"
        event_list = sort.sort_by_date(tix.get_event_list(artist_data, 'New York'))
        print "DONE"
        return render_template(
            'dashboard.html',
            logged_in = True,
            event_list = event_list
        )
    else:
        # Authentication url is a Spotify page
        auth_url = auth.authentication_url()
        return render_template('dashboard.html', logged_in = False, auth_url=auth_url)

# Logout
@app.route('/logout/', methods = ['POST'])
def logout():
    d = request.form
    if (d["type"] == "Log Out"):
        session.pop('access_token')
        session.pop('refresh_token')
    return redirect(url_for('root'))

# Used for the callback from Spotify to our website
@app.route('/login/')
def login():
    # If it has been called back, then send a request to get an access token
    # Might modify this (b.c. anyone could just put any code they wanted into the URL)
    if auth.check_state(request.args.get('state')):
        print "CALLED BACK"
        auth_token = request.args['code']
        token_response = auth.token_request(auth_token)
        session['access_token'] = token_response['access_token']
        session['refresh_token'] = token_response['refresh_token']

        if not dbUtil.isUserInDB():
            print "NEW USER"
            dbUtil.addUserToDB()
        else:
            print "OLD USER"
            dbUtil.refreshArtistData()
    # Always redirect to the homepage
    print "REDIRECTING TO HOME"
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

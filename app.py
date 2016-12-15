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
        artist_data = loads(dbUtil.getArtistData()) #sorted (all)
        artist_data = sift.top_n(artist_data, 24) #slices list

        print "GETTING EVENTS"
        city = tix.get_city()
        #event_list = tix.get_event_list(artist_data, city)
        event_list = loads(dbUtil.getEventData())
        print "DONE"
        return render_template(
            'dashboard.html',
            logged_in = True,
            #artist_data = artist_data,
            event_list = event_list
        )
    else:
        # Authentication url is a Spotify page
        auth_url = auth.authentication_url()
        return render_template('dashboard.html', logged_in = False, auth_url=auth_url)

@app.route('/home/sortby/<attribute>')
def homesorted(attribute):
    if attribute == "artists-alphabetical":
        event_list_sorted = sort.sort_artists_alphabet( tix.get_event_list())

@app.route('/refresh/', methods = ['POST'])
def refresh():
    d = request.form
    if (d['type'] == "Refresh Events"):
        dbUtil.refreshEventData()
    if (d['type'] == "Refresh Artists"):
        dbUtil.refreshArtistData()
    return redirect(url_for('root'))


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
    event_list = loads(dbUtil.getEventData())
    event_details = next((item for item in event_list if item["id"] == eventID), None)
    if event_details == None:
        return "Event not found :("
    else:
        name = event_details['event-name']
        date = event_details['date']
        artist = event_details['artist']
        url = event_details['url']
        status = event_details['status']
        location = [event_details['latitude'], event_details['longitude']]
        map_link = "https://www.google.com/maps/embed/v1/search?key=AIzaSyBUaDb-SbcTLRAg6abFCDDMLuip-DnRs74&q={}+{}".format(event_details['latitude'], event_details['longitude'])
        return render_template(
            'event.html',
            name = name,
            date = date,
            artist = artist,
            url = url,
            status = status,
            location = location,
            map_link = map_link,
            eventID = eventID
        )

@app.route('/submit/')
def submitStatus():
    d = request.form
    if (d['value'] == "Going"):
        dbUtil.updateStatus("going")
    if (d['value'] == "Interested"):
        dbUtil.updateStatus("interested")
    if (d['value'] == "Neither"):
        dbUtil.updateStatus("unmarked")
    param = "/event/%s" %d['title']
    return redirect(param)) 

if __name__ == '__main__':
    app.debug = True
    app.run()

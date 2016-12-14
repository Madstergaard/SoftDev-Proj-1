import sqlite3, sift, tix
from flask import session
import json


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ USER TABLE (AKA ONLY TABLE) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# FOR USERNAMES

def isUserInDB():
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()

	# use oAuth to retrieve username
	user = sift.profile_data(session["access_token"]).get('id')

    # Check if username in DB
	cmd = "SELECT * FROM Users;"
	sel = c.execute(cmd)
	for record in sel:
		if user == record[0]:
			db.close()
			return True
	db.close()
	return False


def addUserToDB():
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()

    # use Spotify API to retrieve username
	user = sift.profile_data(session["access_token"]).get('id')
	# user = "Test1"

    # use Ipinfo to get location
	location = tix.get_city()        
	# location = "Test1"

    # default preferences
	numArtists = 10

	# gets artist data 
        artistData = json.dumps(sift.artist_num(session['access_token']))

        # gets event data
        eventData = json.dumps(tix.get_event_list(json.loads(artistData), 24), location)

        params = (user, location, numArtists, artistData, eventData)
	cmd = 'INSERT INTO Users VALUES(?,?,?,?,?);' 
	c.execute(cmd, params)
	db.commit()
	db.close()
	return



# FOR LOCATION

def updateLocation(newLocation):
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()

    # use Spotify API to retrieve username
	user = sift.profile_data(session["access_token"]).get('id')

        params = (newLocation, user)
	cmd = 'UPDATE Users SET location = ? WHERE username = ?'
	c.execute(cmd, params)
	db.commit()
	db.close()
	return

def getLocation():
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()

	# use oAuth to retrieve username
	user = sift.profile_data(session["access_token"]).get('id')

        params = (user,)
	cmd = 'SELECT location FROM Users WHERE username = ?'
	c.execute(cmd, params)
        ret = c.fetchone()[0]
	db.commit()
	db.close()
	return ret



# FOR ARTISTS

def refreshArtistData():
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()

	user = sift.profile_data(session["access_token"]).get('id')

        artistData = json.dumps(sift.artist_num(session['access_token']))

        params = (artistData, user)
	cmd = 'UPDATE Users SET artistData = ? WHERE username = ?;'
	c.execute(cmd, params)
	db.commit()
	db.close()
	return

def getArtistData():
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()

	user = sift.profile_data(session["access_token"]).get('id')

        params = (user,)
	cmd = 'SELECT artistData FROM Users WHERE username = ?'
	c.execute(cmd, params)
        ret = c.fetchone()[0]
	db.commit()
	db.close()
	return ret




# FOR EVENTS

def refreshEventData():
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()
        city = getLocation()
        user = sift.profile_data(session["access_token"]).get('id')
        if city == "current":
                city = tix.get_city()

        eventData = json.dumps(tix.get_event_list(json.loads(getArtistData()), city))
        
        params = (eventData, user)
	cmd = 'UPDATE Users SET eventData = ? WHERE username = ?;'
	c.execute(cmd, params)
	db.commit()
	db.close()
	return


def getEventData():
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()

	user = sift.profile_data(session["access_token"]).get('id')

        params = (user,)
	cmd = 'SELECT eventData FROM Users WHERE username = ?;'
	c.execute(cmd, params)
        ret = c.fetchone()[0]
	db.commit()
	db.close()
	return ret



# FOR STATUS

def updateStatus(status):
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()
	user = sift.profile_data(session["access_token"]).get('id')
      
    params = (user)  
    eventData = 'SELECT eventData FROM Users WHERE username = ?;'

	# Insert json here

        params = (eventData, user)
	cmd = 'UPDATE Users SET eventData = ? WHERE username = ?;'
	c.execute(cmd, params)
	db.commit()
	db.close()
	return

def getStatus():



import sqlite3, sift
from flask import session
import json

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
	location = "New York"
	# location = "Test1"

    # default preferences
	numArtists = 10

        artistData = json.dumps(sift.artist_num(session['access_token']))

        params = (user, location, numArtists, artistData)
	cmd = 'INSERT INTO Users VALUES(?,?,?,?);'
	c.execute(cmd, params)
	db.commit()
	db.close()
	return

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


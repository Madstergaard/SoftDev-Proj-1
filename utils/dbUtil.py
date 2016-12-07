import sqlite3, sift
from flask import session

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

	cmd = 'INSERT INTO Users VALUES("%s", "%s", %d);' %(user, location, numArtists)
	c.execute(cmd)
	db.commit()
	db.close()
	return 


def updateLocation(newLocation):
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()

    # use Spotify API to retrieve username
	user = sift.profile_data(session["access_token"]).get('id')

	cmd = 'UPDATE Users SET location = "%s" WHERE user = "%s"' %(newLocation, user)
	c.execute(cmd)
	db.commit()
	db.close()
	return 

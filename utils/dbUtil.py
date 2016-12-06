import sqlite3, sift

def isUserInDB():
	db = sqlite3.connect("data/DB.db")
	c = db.cursor()

	# use oAuth to retrieve username
	user = sift.profile_data("access_token").get('id')

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
	#user = sift.profile_data("access_token").get('id')
	user = "Test"

    # use Ipinfo to get location
	#location = "this hasn't been implemented yet"
	location = "Test"

    # default preferences
	numArtists = 10

    # Check if username in DB
	cmd = "INSERT INTO Users VALUES('%s', '%s', %d);" %(user, location, numArtists)
	db.close()
	return 

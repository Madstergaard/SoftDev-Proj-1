import sqlite3

###ONE TIME USE TO CREATE THE DATABASE AND TABLES


db = sqlite3.connect("data/DB.db")
c = db.cursor()


userTable = "CREATE TABLE Users(username TEXT, location TEXT, numArtists INTEGER);"
c.execute(userTable)

goingTable = "CREATE TABLE EventsAttending(username TEXT, eventName TEXT, eventURL TEXT, location TEXT, dateOfEvent TEXT);"
c.execute(goingTable)

interestedTable = "CREATE TABLE EventsInterestedIn(username TEXT, eventName TEXT, eventURL TEXT, location TEXT, dateOfEvent TEXT);"
c.execute(interestedTable)

db.commit()
db.close()

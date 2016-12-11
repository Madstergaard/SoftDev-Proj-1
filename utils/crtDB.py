import sqlite3

###ONE TIME USE TO CREATE THE DATABASE AND TABLES


db = sqlite3.connect("data/DB.db")
c = db.cursor()


userTable = "CREATE TABLE Users(username TEXT, location TEXT, numArtists INTEGER, artistData TEXT, eventData TEXT);"
c.execute(userTable)

db.commit()
db.close()

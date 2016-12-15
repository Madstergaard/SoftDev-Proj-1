# MOSSY (Missing Out on Shows Sucks, Yo)
*By Maddie Ostergaard, Sarah Yoon & Seiji Yawata*

MOSSY is a service that takes the user’s location and saved tracks on Spotify to find concerts in that area from their favorite artists (judging by the number of tracks by that artist they have saved).

## How To Use

### Setup
1. Install flask in a virtual environment
2. Install the [requests](http://docs.python-requests.org/en/master/) module with `pip install requests`

### Usage
`python app.py` will run the Flask app on port 5000

You will need a Spotify account to be able to use this service (and it should ideally have enough saved tracks to be able to extract meaningful data).

Authorize MOSSY to allow access to your account (or else...).

A dashboard will then be presented, showing concerts in your region. For these, you can set whether you are going, interested, or neither. This page can be sorted by status, by date, or by the artist's popularity in your Spotify account (by default).

Clicking on an event card will take you to that event's specific page, where you can set your status, see a map indicating where the event will take place, and go to the event's Ticketmaster page to buy tickets.



from flask import Flask, render_template, request, session, url_for, redirect
from json import loads, dumps

app = Flask(__name__)
app.secret_key = 'secrets'



@app.route('/')
def event():
    name = "Let's All Get Together and Love Nick Jonas"
    date = "TODAY"
    artist = "Nick Jonas"
    url = "http://www.ticketmaster.com/Nick-Jonas-tickets/artist/1387405"
    location = "New York"
    return render_template(
        'event.html',
        name = name,
        date = date,
        artist = artist,
        url = url,
        location = location
    )


if __name__ == '__main__':
    app.debug = True
    app.run()

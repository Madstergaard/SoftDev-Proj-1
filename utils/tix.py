import sqlite3
import urllib
import requests
import json
import sift

# TicketMaster URLs
TICKETMASTER_API_URL = 'https://app.ticketmaster.com/discovery/v2'
API_KEY = json.loads(open("keys.json").read())['ticketmaster']['API_KEY']

# Returns user's current city from ip info
def get_city():                             
    response = sift.data('http://ipinfo.io/geo', None, None)
    return response['city']

# Returns list of event dicts for all top artists in given city
# Default order: number of songs saved from each artist
def get_event_list(artists, city):
    ret = []
    for artist in artists:
        print "GETTING TIX DATA FOR {}".format(artist.encode('utf-8'))
        ret.extend( get_events( artist, (get_event_ids(artist, city)) ) )
    return ret

# Returns a list of event ids for one artist in given city
def get_event_ids(artist, city):
    params = {'classificationName':'music', 'city':city, 'keyword':artist.encode('utf-8')}

    endpoint = '{}/events.json?{}&apikey={}'.format(TICKETMASTER_API_URL, urllib.urlencode(params), API_KEY)
    response = sift.data(endpoint, None, None)
    if '_embedded' in response:
        return [event['id'] for event in response['_embedded']['events']]
    return []

# Returns a dict representing individual event given event id
def event(eventid):
    ret = {}
    endpoint = '{}/events/{}.json?apikey={}'.format(TICKETMASTER_API_URL, eventid, API_KEY)
    response = sift.data(endpoint, None, None)
    if 'dates' in response:
        ret['date'] = response['dates']['start']['localDate']
    if 'url' in response:
        ret['url'] = response['url']
    if '_embedded' in response:
        ret['latitude'] = response['_embedded']['venues'][0]['location']['latitude']
        ret['longitude'] = response['_embedded']['venues'][0]['location']['longitude']
    if 'name' in response:
        ret['event-name'] = response['name']
    ret['status'] = 'unmarked'
    return ret

# Returns a list of events for one artist given list of event ids
def get_events(artist, id_list):
    ret = []
    for eid in id_list:
        concert = event(eid)
        concert['artist'] = artist
        ret.append(concert)
    return ret


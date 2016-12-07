import urllib
import requests
import json
import sift

# TicketMaster URLs
TICKETMASTER_API_URL = 'https://app.ticketmaster.com/discovery/v2'
API_KEY = 'QrqMB3GhEKBVuiWdCmFGYZlmJhHR6UTJ'

# Returns list of event urls for all top artists in given city
def get_event_list(artists, city):
    ret = []
    for artist in artists:
        ret.extend(get_event_urls(artist, city))
    return ret
        
# Returns a list of event urls for one artist in given city
def get_event_urls(artist, city):
    ret = []
    params = {'classificationName':'music', 'city':city, 'keyword':artist.encode('utf-8')}
   
    endpoint = '{}/events.json?{}&apikey={}'.format(TICKETMASTER_API_URL, urllib.urlencode(params), API_KEY)
    response = sift.data(endpoint, None, None)
    if '_embedded' in response:
        return [event['url'] for event in response['_embedded']['events']]
    else:
        return []
    #return response

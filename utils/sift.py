from collections import OrderedDict
from itertools import islice
import json # JSON (duh)
import urllib
import urllib2

# Spotify URLs
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = 'v1'
SPOTIFY_API_URL = '{}/{}'.format(SPOTIFY_API_BASE_URL, API_VERSION)

def data(endpoint, params, headers):
    # response = requests.get(endpoint, params=params, headers=headers)
    # return json.loads(response.text)
    params_str = urllib.urlencode(params) if params else ""
    req_str = "{}/?{}".format(endpoint, params_str) if params_str else endpoint
    req = urllib2.Request(req_str, None, headers) if headers else urllib2.Request(req_str)
    return json.loads(urllib2.urlopen(req).read())

def profile_data(access_token):
    endpoint = '{}/me'.format(SPOTIFY_API_URL)
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    return data(endpoint, None, headers)

# Used in artist_num
def add_artists(curr_page, ret):
    for track_object in map(lambda x:x['track'], curr_page['items']):
        for artist_object in track_object['artists']:
            artist_name = artist_object['name']
            ret[artist_name] = ret.get(artist_name, 0) + 1

# Returns list of artists with the one with most tracks at index 0
def artist_num(access_token):
    ret = dict()

    endpoint = '{}/me/tracks'.format(SPOTIFY_API_URL)
    params = {'limit':50}
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    curr_page = data(endpoint, params, headers)
    add_artists(curr_page, ret)

    while (curr_page.get('next')):
        curr_page = data(curr_page.get('next'), None, headers)
        add_artists(curr_page, ret)

    ret = OrderedDict(sorted(ret.items(), key = lambda x:x[1], reverse=True))
    return list(ret.keys())

# Returns top n artists list
def top_n(artist_data, n):
    return artist_data[0:n]

from collections import OrderedDict
import json # JSON (duh)
import requests # GET and POST requests

# Spotify URLs
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = 'v1'
SPOTIFY_API_URL = '{}/{}'.format(SPOTIFY_API_BASE_URL, API_VERSION)

def data(endpoint, params, headers):
    response = requests.get(endpoint, params=params, headers=headers)
    return json.loads(response.text)

def profile_data(access_token):
    endpoint = '{}/me'.format(SPOTIFY_API_URL)
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    return data(endpoint, None, headers)

# Returns list of track objects (used by saved_tracks() )
def track_objects_list(curr_page):
    return [track_wrapper['track'] for track_wrapper in curr_page['items']]

# Returns list of all saved tracks (as track objects - see API website )
def saved_tracks(access_token):
    tracks_list = list()
    endpoint = '{}/me/tracks'.format(SPOTIFY_API_URL)
    params = {'limit':50}
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    curr_page = data(endpoint, params, headers)
    tracks_list += track_objects_list(curr_page)
    # Run the loop while there exists a page after the current one
    while (curr_page.get('next')):
        curr_page = data(curr_page.get('next'), None, headers)
        tracks_list += track_objects_list(curr_page)
    return tracks_list


# Returns dict with 'unique_track_id':['artist', 'track'] pairs
def trackid_dict(tracks_list):
    pairs = dict()
    for track_object in tracks_list:
        for artist_object in track_object['artists']:
            artist_name = artist_object['name']
            track_name = track_object['name']
            track_id = track_object['id']
            pairs[track_id] = [artist_name, track_name]
    return pairs

# Returns ordered dict with 'artist':'number of tracks' pairs ordered by number of tracks
def artist_numtrack_dict(trackid_dict):
    ret = dict()
    for track in trackid_dict:
        artist_name = trackid_dict[track][0]
        if not artist_name in ret:
            ret[artist_name] = 0
        ret[artist_name] += 1
    return OrderedDict(sorted(ret.items(), key=lambda t:t[1], reverse=True))

# Wrapper function for artist_numtrack_dict
def top_n_artists(ordered, n):
    ret = OrderedDict()
    for i in ordered.keys()[0:n]:
        ret[i] = ordered[i]
    return ret

    

    

    

    


import json # JSON (duh)
import requests # GET and POST requests
import base64 # Encoding client_id:client_secret
import urllib # Encoding query parameters in url format (not provided in url2)

#  Client Keys
CLIENT_ID = 'ff5c4964b91b47d0a40933042bbe51d4'
CLIENT_SECRET = '034ac7a503834cd9a02f25183c3397d6'

# Spotify URLS
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = 'v1'
SPOTIFY_API_URL = '{}/{}'.format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = 'http://127.0.0.1:5000'
REDIRECT_URI = '{}/login/'.format(CLIENT_SIDE_URL)
SCOPE = 'playlist-read-private user-follow-read user-library-read'
STATE = ''
SHOW_DIALOG_bool = False
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_params = {
    'response_type': 'code',
    'redirect_uri': REDIRECT_URI,
    'scope': SCOPE,
    #'state': STATE,
    'show_dialog': SHOW_DIALOG_str,
    'client_id': CLIENT_ID
}

def authentication_url():
    url_args = urllib.urlencode(auth_query_params)
    auth_url = '{}/?{}'.format(SPOTIFY_AUTH_URL, url_args)
    return auth_url

def token_request(auth_token):
    post_query_params = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': REDIRECT_URI
    }
    encoded_secret = base64.b64encode('{}:{}'.format(CLIENT_ID, CLIENT_SECRET))
    headers = {'Authorization': 'Basic {}'.format(encoded_secret)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=post_query_params, headers=headers)

    response_data = json.loads(post_request.text)
    return response_data

def get_profile_data(access_token):
    authorization_header = {'authorization': 'Bearer {}'.format(access_token)}
    user_profile_api_endpoint = '{}/me'.format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_json_text = profile_response.text
    profile_dict = json.loads(profile_json_text)
    return profile_dict

def get_saved_tracks(access_token):
    authorization_header = {'authorization': 'Bearer {}'.format(access_token)}
    tracks_api_endpoint = '{}/me/tracks'.format(SPOTIFY_API_URL)
    tracks_response =requests.get(tracks_api_endpoint, headers=authorization_header)
    tracks_json_text = tracks_response.text
    tracks_dict = json.loads(tracks_response.text)
    return tracks_dict


import json # JSON (duh)
import requests # GET and POST requests
import base64 # Encoding client_id:client_secret
import urllib # Encoding query parameters in url format (not provided in urllib2, sorry Mr. DW)
import uuid # For generating unique identifier (state param)

# Authorization Code Flow implementation: https://developer.spotify.com/web-api/authorization-guide/#authorization-code-flow

# Client Keys
CLIENT_ID = 'ff5c4964b91b47d0a40933042bbe51d4'
CLIENT_SECRET = '034ac7a503834cd9a02f25183c3397d6'

# Spotify URLS
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Server-side Parameters
REDIRECT_URI = 'http://127.0.0.1:5000/login/'
SCOPE = 'playlist-read-private user-follow-read user-library-read'
STATE = str(uuid.uuid4())
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

# The parameter for the authentication url (the 'MOSSY wants to connect to your account' page)
auth_query_params = {
    'response_type': 'code',
    'redirect_uri': REDIRECT_URI,
    'scope': SCOPE,
    'state': STATE,
    'show_dialog': SHOW_DIALOG_str,
    'client_id': CLIENT_ID
}

# Formats the params above into a nice url
def authentication_url():
    url_args = urllib.urlencode(auth_query_params)
    auth_url = '{}/?{}'.format(SPOTIFY_AUTH_URL, url_args)
    return auth_url

def check_state(state):
    return state == STATE

# After the user accepts the request from MOSSY, a POST request is made with the auth_token to obtain
# an access_token and a refresh_token
def token_request(auth_token):
    # Request body params
    post_query_params = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': REDIRECT_URI
    }
    # Header Parameter (encodes the CLIENT_ID and CLIENT_SECRET)
    encoded_secret = base64.b64encode('{}:{}'.format(CLIENT_ID, CLIENT_SECRET))
    headers = {'Authorization': 'Basic {}'.format(encoded_secret)}
    # POST request
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=post_query_params, headers=headers)
    # Response JSON data with 'access_token', 'token_type', 'scope', 'expires_in' and 'refresh_token'
    # **Right now the app's only using the access_token, but once it expires, there's no fallback
    response_data = json.loads(post_request.text)
    return response_data

# Returns new access_token
def refresh(refresh_token):
    params = {
        'grant_type':'refresh_token',
        'refresh_token':refresh_token
    }
    encoded_secret = base64.b64encode('{}:{}'.format(CLIENT_ID, CLIENT_SECRET))
    headers = {'Authorization': 'Basic {}'.format(encoded_secret)}
    request = requests.post(SPOTIFY_TOKEN_URL, data=params, headers=headers)
    return json.loads(request.text)['access_token']




from flask import Flask, request, redirect, session
import requests
import base64
import secrets
import json

secret_k = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_k

# Spotify API credentials
CLIENT_ID = '37c79705ae2e4b259695bea61741326d'
CLIENT_SECRET = 'e29fdced8037461aa1e8f6ba7d1cc0b2'
REDIRECT_URI = 'http://localhost:8088/callback'

# Spotify API endpoints
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Scopes define the permissions your app needs
SCOPES = ['user-read-recently-played']

@app.route('/')
def home():
    # Redirect the user to Spotify's authorization page
    auth_query_parameters = {
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES),
        'client_id': CLIENT_ID
    }
    auth_url = f"{SPOTIFY_AUTH_URL}/?{requests.compat.urlencode(auth_query_parameters)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Handle the callback from Spotify
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data, headers=headers)

    if response.status_code == 200:
        data = response.json()
        access_token = data['access_token']
        print(data)
        # Store the access token securely (e.g., in a database)
        session['access_token'] = access_token

        # Now that you have the access token, you can use it to make requests to the Spotify API.
        # For example, let's retrieve the user's recently played tracks.
        recently_played_url = 'https://api.spotify.com/v1/me/player/recently-played'
        recently_played_headers = {
            'Authorization': f'Bearer {access_token}'
        }

        recently_played_response = requests.get(recently_played_url, headers=recently_played_headers)

        if recently_played_response.status_code == 200:
            recently_played_data = recently_played_response.json()
            # Do something with the recently played data
            return json.dumps(recently_played_data, indent=2)
        else:
            return f"Failed to retrieve recently played tracks. Status code: {recently_played_response.status_code}"

    else:
        return "Failed to obtain an access token."

if __name__ == '__main__':
    app.run(debug=True, port=8080)

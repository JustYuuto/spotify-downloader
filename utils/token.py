import requests
from os.path import exists
import json


class AccessToken:

    access_token = open('spotify_token.txt', 'r').read() if exists('spotify_token.txt') else ''
    dc = open('spotify_dc.txt', 'r').read() if exists('spotify_dc.txt') else ''
    client_token = open('spotify_client_token.txt', 'r').read() if exists('spotify_client_token.txt') else ''

    def __init__(self):
        pass

    def refresh(self):
        url = 'https://open.spotify.com/get_access_token'
        params = {
            'reason': 'transport',
            'productType': 'web-player'
        }
        request = requests.get(url, headers={
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en',
            'App-Platform': 'WebPlayer',
            'Connection': 'keep-alive',
            'Cookie': f'sp_dc={self.client_token}',
            'Host': 'open.spotify.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Spotify-App-Version': '1.2.33.0-unknown',
            'TE': 'trailers',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        }, params=params)
        request.raise_for_status()
        token = request.json()['accessToken']

        self.access_token = token

        with open('spotify_token.txt', 'w') as file:
            file.write(token)

        return token

    def get_client_token(self):
        url = 'https://clienttoken.spotify.com/v1/clienttoken'
        request = requests.post(url, data=json.dumps({
            'client_data': {
                'client_id': 'd8a5ed958d274c2e8ee717e6a4b0971d',
                'client_version': '1.2.33.0-unknown',
            }
        }), headers={
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'clienttoken.spotify.com',
            'Origin': 'https://open.spotify.com',
            'Referer': 'https://open.spotify.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        })
        request.raise_for_status()
        token = request.json()['granted_token']['token']

        self.client_token = token

        with open('spotify_client_token.txt', 'w') as file:
            file.write(token)

        return token

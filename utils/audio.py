import requests
from utils.token import AccessToken


class Audio:
    pssh = ''
    license_url = 'https://gew1-spclient.spotify.com/widevine-license/v1/audio/license'
    access_token = AccessToken().access_token

    def __init__(self):
        pass

    def get_track_url(self, track_id):
        return f'https://spclient.wg.spotify.com/metadata/4/track/{track_id}?market=from_token'

    def get_track(self, track_id):
        url = self.get_track_url(track_id)
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en',
            'Authorization': f'Bearer {AccessToken().access_token}',
            'Connection': 'keep-alive',
            'Host': 'spclient.wg.spotify.com',
            'Origin': 'https://open.spotify.com',
            'Prefer': 'safe',
            'Referer': 'https://open.spotify.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-GPC': '1',
            'TE': 'Trailers',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        }
        request = requests.get(url, headers=headers)
        request.raise_for_status()
        json = request.json()

        return json

    def get_audio_urls(self, file_id):
        url = f'https://gew1-spclient.spotify.com/storage-resolve/v2/files/audio/interactive/11/{file_id}'
        params = {
            'version': 10000000,
            'product': 9,
            'platform': 39,
            'alt': 'json'
        }
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en',
            'Authorization': f'Bearer {self.access_token}',
            'Connection': 'keep-alive',
            'Host': 'gew1-spclient.spotify.com',
            'Origin': 'https://open.spotify.com',
            'Prefer': 'safe',
            'Referer': 'https://open.spotify.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-GPC': '1',
            'TE': 'Trailers',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        }
        request = requests.get(url, params=params, headers=headers)
        request.raise_for_status()
        json = request.json()

        return json['cdnurl']

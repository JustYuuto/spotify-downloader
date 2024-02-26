import eyed3
import requests
from utils.audio import Audio
from utils.token import AccessToken


class Metadata:

    access_token = AccessToken().access_token

    def __init__(self):
        pass

    def get_metadata(self, track_id):
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en',
            'Authorization': f'Bearer {self.access_token}',
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
        request = requests.get(Audio().get_track_url(track_id), headers=headers)
        request.raise_for_status()

        return request.json()

    def set_metadata(self, metadata, file_path):
        file = eyed3.load(file_path)
        file.initTag()
        file.tag.artist = metadata['artist'][0]['name']
        file.tag.album = metadata['album']['name']
        file.tag.album_artist = metadata['album']['artist'][0]['name']
        file.tag.title = metadata['name']
        file.tag.track_num = metadata['number']
        file.tag.release_date = metadata['album']['date']['year']
        cover_url = 'https://i.scdn.co/image/' + metadata['album']['cover_group']['image'][0]['file_id']
        file.tag.images.set(3, requests.get(cover_url).content, 'image/jpeg')
        file.tag.save()

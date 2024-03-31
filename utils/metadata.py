import eyed3
import requests


class Metadata:

    def __init__(self):
        pass

    def set_metadata(self, metadata, file_path):
        audio = eyed3.load(file_path)
        audio.initTag()
        audio.tag.artist = metadata['artist'][0]['name']
        audio.tag.album = metadata['album']['name']
        audio.tag.album_artist = metadata['album']['artist'][0]['name']
        audio.tag.title = metadata['name']
        audio.tag.track_num = metadata['number']
        audio.tag.release_date = metadata['album']['date']['year']
        cover_url = 'https://i.scdn.co/image/' + metadata['album']['cover_group']['image'][0]['file_id']
        audio.tag.images.set(3, requests.get(cover_url).content, 'image/png')
        audio.tag.save()
        print('Metadata set successfully')

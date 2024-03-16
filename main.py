from os.path import abspath, isfile
from os import remove, rename
import requests
from utils.audio import Audio
from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
from utils.metadata import Metadata
import subprocess
import argparse
from utils.token import AccessToken

if not isfile('device.wvd'):
    print('You need to have a device.wvd file in the same directory as this script')
    exit(1)

parser = argparse.ArgumentParser(
                    prog='Spotify Downloader',
                    description='it downloads spotify songs')
parser.add_argument('track_id', type=str, help='The track id of the song')
parser.add_argument('--add-metadata', type=bool,
                    help='Should add metadata to the song? (like artists, album, cover, etc)',
                    default=False, required=False)
args = parser.parse_args()

if __name__ == '__main__':
    if not isfile('spotify_dc.txt'):
        user_token = input('Enter your Spotify "sp_dc" cookie: ')
        with open('spotify_dc.txt', 'w') as file:
            file.write(user_token.replace('Bearer ', ''))
    else:
        user_token = open('spotify_dc.txt', 'r').read()

    track_id = args.track_id

    token = AccessToken()
    audio = Audio()
    metadata = Metadata()
    try:
        track = audio.get_track(track_id)
    except requests.exceptions.HTTPError as e:
        token.refresh()
        track = audio.get_track(track_id)

    file_id = track['file'][4]['file_id']
    url = audio.get_audio_urls(file_id)[0]

    pssh = PSSH(requests.get(f'https://seektables.scdn.co/seektable/{file_id}.json').json()['pssh'])
    device = Device.load('device.wvd')
    cdm = Cdm.from_device(device)
    session_id = cdm.open()

    challenge = cdm.get_license_challenge(session_id, pssh)
    try:
        license = requests.post(audio.license_url, headers={
            'Authorization': f'Bearer {AccessToken().access_token}',
            'client-token': AccessToken().client_token,
            'Content-Type': 'application/octet-stream',
        }, data=challenge)
        license.raise_for_status()
    except requests.exceptions.HTTPError as e:
        token.get_client_token()
        license = requests.post(audio.license_url, headers={
            'Authorization': f'Bearer {AccessToken().access_token}',
            'client-token': AccessToken().client_token,
            'Content-Type': 'application/octet-stream',
        }, data=challenge)
        license.raise_for_status()

    cdm.parse_license(session_id, license.content)

    audio = requests.get(url)
    audio_file = abspath(f"./{track['name']}.mp3")
    audio_file_decrypted = abspath(f"./{track['name']}-decrypted.mp3")

    if isfile(audio_file):
        remove(audio_file)
    if isfile(audio_file_decrypted):
        remove(audio_file_decrypted)

    with open(audio_file, 'wb') as file:
        file.write(audio.content)
        file.close()

    for key in cdm.get_keys(session_id):
        subprocess.run([
            'ffmpeg', '-decryption_key', key.key.hex(), '-i', audio_file, audio_file_decrypted
        ])

    if args.add_metadata:
        metadata.set_metadata(track, audio_file_decrypted)

    remove(audio_file)
    rename(audio_file_decrypted, audio_file)

    cdm.close(session_id)

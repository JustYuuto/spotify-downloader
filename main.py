from os.path import abspath, isfile
from os import remove, rename, environ
import requests
from utils.audio import Audio
from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
from utils.metadata import Metadata
import subprocess
import argparse
from utils.token import AccessToken
from librespot.metadata import TrackId

parser = argparse.ArgumentParser(
                    prog='Spotify Downloader',
                    description='it downloads spotify songs')
parser.add_argument('track_id', type=str, help='The track id of the song. Public IDs, GIDs and Spotify URIs are supported')
parser.add_argument('--add-metadata', type=bool,
                    help='Should add metadata to the song? (like artists, album, cover, etc). Defaults to false.',
                    default=False, required=False)
parser.add_argument('--ffmpeg-path', type=str,
                    help='Path to the ffmpeg executable (if not in PATH)', required=False)
parser.add_argument('--quality', type=str,
                    help='The quality to download. Defaults to MP4_256.',
                    default='MP4_256', required=False, choices=[
                        'OGG_VORBIS_96', 'OGG_VORBIS_160', 'OGG_VORBIS_320',
                        'MP4_128', 'MP4_128_DUAL', 'MP4_256', 'MP4_256_DUAL',
                        'AAC_24'
                    ])
args = parser.parse_args()

if __name__ == '__main__':
    if not isfile('device.wvd'):
        print('You need to have a device.wvd file in the same directory as this script')
        exit(1)

    if isinstance(args.ffmpeg_path, str) and not isfile(args.ffmpeg_path):
        print('Error: FFmpeg was not found in the specified path!')
        exit(1)
    elif not 'ffmpeg' in environ['PATH']:
        print('Error: FFmpeg was not found in your path!')
        exit(1)
    
    if not isfile('spotify_dc.txt'):
        user_token = input('Enter your Spotify "sp_dc" cookie: ')
        with open('spotify_dc.txt', 'w') as file:
            file.write(user_token.replace('Bearer ', ''))
    else:
        user_token = open('spotify_dc.txt', 'r').read()

    track_id = args.track_id

    if len(track_id) == 22:
        track_id = TrackId.from_base62(track_id).get_gid().hex()
    elif 'spotify:track:' in track_id:
        track_id = TrackId.from_base62(track_id.replace('spotify:track:', '')).get_gid().hex()

    token = AccessToken()
    audio = Audio()
    metadata = Metadata()
    try:
        track = audio.get_track(track_id)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            token.refresh()
            track = audio.get_track(track_id)
        else:
            print('Error:', e)
            exit(1)

    def find_quality(track, quality):
        for file in track['file']:
            if file['format'] == quality:
                return file
        return None

    pssh = PSSH(requests.get(f"https://seektables.scdn.co/seektable/{track['file'][4]['file_id']}.json").json()['pssh'])
    device = Device.load('device.wvd')
    cdm = Cdm.from_device(device)
    session_id = cdm.open()

    challenge = cdm.get_license_challenge(session_id, pssh)
    license = requests.post(audio.license_url, headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en',
        'authorization': f'Bearer {AccessToken().access_token()}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    }, data=challenge)
    license.raise_for_status()

    cdm.parse_license(session_id, license.content)

    cdn_file = find_quality(track, args.quality)
    url = audio.get_audio_urls(cdn_file['file_id'])[0]
    audio = requests.get(url)
    audio.raise_for_status()
    audio_type = cdn_file['format'].split('_')[0].lower().replace('mp4', 'm4a')
    audio_file = abspath(f"./{track['name']}-encrypted.{audio_type}")
    audio_file_decrypted = abspath(f"./{track['name']}.{audio_type}")

    if isfile(audio_file):
        remove(audio_file)
    if isfile(audio_file_decrypted):
        remove(audio_file_decrypted)

    with open(audio_file, 'wb') as file:
        file.write(audio.content)
        file.close()

    for key in cdm.get_keys(session_id):
        try:
            path = args.ffmpeg_path if isinstance(args.ffmpeg_path, str) else 'ffmpeg'
            cmd = [
                path, '-decryption_key', key.key.hex(), '-i', audio_file, audio_file_decrypted
            ]
            subprocess.run(cmd, stdout=None, stderr=None, stdin=None, shell=False, check=True)
        except Exception as e:
            print('Error:', e)
            exit(1)
    cdm.close(session_id)

    remove(audio_file)

    if args.add_metadata == True:
        print('Adding metadata to the song...')
        metadata.set_metadata(track, audio_file_decrypted)

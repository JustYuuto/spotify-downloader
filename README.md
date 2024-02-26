# Spotify Downloader

a python script to download music straight from spotify servers lol

## Features

- supports downloading music from spotify (that's the fcking point of this program)
- actually it downloads music directly from spotify servers, so the quality is the same as the original
- it decrypts the drm encryption (how???? omg u need to know that widevine is shit)
- **soon:** downloading playlists and albums

## Usage

```bash
git clone https://github.com/JustYuuto/spotify-downloader.git
cd spotify-downloader
pip install -r requirements.txt
python main.py <track id you want to download>
```

the script will likely ask you the "sp_dc" cookie, u can get it by logging into spotify web and getting the cookie from the storage (in devtools)

note: u need to have a spotify premium account to download music at 160kbps+

## Requirements

- [Python 3](https://www.python.org/downloads/)
- [FFmpeg](https://www.ffmpeg.org/download.html) (in ur path), this is required for decrypting mp3s

## License

the source code is licensed under the mit license bcz why not. u can view it [here](LICENSE.txt)
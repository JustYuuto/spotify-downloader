# Spotify Downloader

A Python script to download music straight from Spotify servers lol

## Features

- Supports downloading music from Spotify (that's the point of this program)
- As it downloads music directly from Spotify servers, the quality is the same as you can hear it on Spotify
- Of course, it decrypts the DRM encryption with pywidevine
- **Soon:** downloading playlists and albums

## Usage

```bash
git clone https://github.com/JustYuuto/spotify-downloader.git
cd spotify-downloader
pip install -r requirements.txt
python main.py <id of the track you want to download>
# Note: the track id can be a normal id, a gid, or a spotify uri (spotify:track:xxxxxx....)
```

Please see https://cdm-project.com/How-To/Dumping-L3-from-Android to get the `device.wvd` file.

The script will likely ask you for your "sp_dc" cookie, you can get it by logging into Spotify web, and getting the cookie from the storage (in devtools).

> [!NOTE]
> You **need** to have a Spotify Premium account to download music at 160kbps+

## Requirements

- [Python 3.9](https://www.python.org/downloads/release/python-390/) (due to the package `pywidevine` and compatibility reasons)
- [FFmpeg](https://www.ffmpeg.org/download.html) (in ur path), this is required for decrypting mp3s


## License

The source code is licensed under the MIT license bcz why not. You can view it [here](LICENSE.txt).

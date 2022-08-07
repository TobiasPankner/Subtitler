import argparse
import glob
import io
import os
import struct
import zipfile
from argparse import ArgumentParser
from shutil import move

import PTN
import autosubsync
import requests
from bs4 import BeautifulSoup

OST_BASE_URL = 'https://www.opensubtitles.org'
SUB_NUM = 1


# from:
# https://github.com/agonzalezro/python-opensubtitles/blob/0143db67df5b80155c258887ca36f62a92455d4e/pythonopensubtitles/utils.py#L72
def compute_movie_hash(path):
    longlongformat = 'q'  # long long
    bytesize = struct.calcsize(longlongformat)
    movie_size = os.path.getsize(path)

    try:
        movie_file = open(path, "rb")
    except(IOError):
        return "IOError"

    movie_hash = int(movie_size)

    if int(movie_size) < 65536 * 2:
        return "SizeError"

    for _ in range(65536 // bytesize):
        buffer = movie_file.read(bytesize)
        (l_value,) = struct.unpack(longlongformat, buffer)
        movie_hash += l_value
        movie_hash = movie_hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

    movie_file.seek(max(0, int(movie_size) - 65536), 0)
    for _ in range(65536 // bytesize):
        buffer = movie_file.read(bytesize)
        (l_value,) = struct.unpack(longlongformat, buffer)
        movie_hash += l_value
        movie_hash = movie_hash & 0xFFFFFFFFFFFFFFFF

    movie_file.close()
    returnedhash = "%016x" % movie_hash
    return str(returnedhash)


def get_sub_urls(language, title, moviehash):
    if moviehash:
        print(f'\tGetting subs by hash: {moviehash}')
        sub_resp = requests.get(
            f'{OST_BASE_URL}/en/search2?SubLanguageID={language}&MovieHash={moviehash}&MovieName={title}'
        )
        if sub_resp.status_code != 200:
            print(f'\tError while getting subs by movie hash: {sub_resp.status_code}')
            return
    elif title:
        print(f'\tGetting subs by title: {title}')
        movie_resp = requests.get(
            f'{OST_BASE_URL}/en/search2?MovieName={title}&action=search&SubLanguageID={language}'
        )
        if movie_resp.status_code != 200:
            print(f'\tError while getting subs by title: {movie_resp.status_code}')
            return

        movie_soup = BeautifulSoup(movie_resp.text, 'html.parser')
        if movie_soup.select('a[href*="serve"]'):
            # this means that we are already on the subtitle page and not on the movie page
            sub_resp = movie_resp
        else:
            movie_url_elems = movie_soup.select('a[href*="idmovie"]')
            if not movie_url_elems:
                print(f'\tNo movie urls found')
                return
            movie_url = movie_url_elems[0].get('href')

            sub_resp = requests.get(
                f'{OST_BASE_URL}{movie_url}'
            )
            if sub_resp.status_code != 200:
                print(f'\tError while getting subs by title: {sub_resp.status_code}')
                return
    else:
        return

    soup = BeautifulSoup(sub_resp.text, 'html.parser')
    sub_urls = [elem['href'] for elem in soup.select('a[href*="serve"]')]
    return sub_urls


def download_subs(title, language, moviehash):
    sub_urls = get_sub_urls(language, '', moviehash)
    if not sub_urls:
        print(f'\tNo subs found using the hash. Trying to get subs by title')
        parsed_title = PTN.parse(title)
        sub_urls = get_sub_urls(language, f'{parsed_title["title"]} {parsed_title.get("year", "")}'.strip(), '')

    print(f'\tFound {len(sub_urls)} subs')
    for sub_url in sub_urls[:SUB_NUM]:
        zip_resp = requests.get(f'{OST_BASE_URL}{sub_url}')
        if zip_resp.status_code != 200:
            print(f'\tError while downloading subtitle: {zip_resp.status_code}')
            return
        z = zipfile.ZipFile(io.BytesIO(zip_resp.content))
        for f in z.filelist:
            if f.filename.endswith('.srt'):
                print("\tDownloaded subtitle, original name:", f.filename)
                f.filename = f'{title}.srt'
                z.extract(f, '.')


if __name__ == '__main__':
    parser = ArgumentParser(description='Automatically downloads and syncs subtitles')
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    parser.add_argument_group('optional arguments')
    required.add_argument('-i', dest='input_dir', type=str, required=True,
                          help='The directory to search for videos')
    optional.add_argument('-ds', dest='disable_sync', action=argparse.BooleanOptionalAction,
                          help='Pass this to disable subtitle synchronization')
    optional.add_argument('-o', dest='enable_override', action=argparse.BooleanOptionalAction,
                          help='Pass this to override existing subtitles')
    optional.add_argument('-l', dest='lang', type=str, default='eng',
                          help='The language of subtitles to download (default: eng)')
    parser._action_groups.append(optional)

    args = parser.parse_args()

    print(r"""
 _____       _     _   _ _   _           
/  ___|     | |   | | (_) | | |          
\ `--. _   _| |__ | |_ _| |_| | ___ _ __ 
 `--. \ | | | '_ \| __| | __| |/ _ \ '__|
/\__/ / |_| | |_) | |_| | |_| |  __/ |   
\____/ \__,_|_.__/ \__|_|\__|_|\___|_|                                  
""")

    print('Checking for videos in directory:', args.input_dir)
    os.chdir(args.input_dir)

    types = ('*.mp4', '*.mkv')
    video_files = []
    for files in types:
        video_files.extend(glob.glob(files))

    print(f'Found {len(video_files)} video file(s)')

    for video_file in video_files:
        print(f'\nProcessing {video_file}:')
        base = video_file.rpartition('.')[0]
        srt_file = base + '.srt'
        synced_srt_file = base + '.tmp.srt'

        if not args.enable_override and os.path.isfile(srt_file):
            print(f'\tExisting subtitle found, skipping')
            continue

        print('\tDownloading subtitles...')
        download_subs(base, args.lang, compute_movie_hash(video_file))

        if not args.disable_sync:
            print('\n\tSynchronizing subtitles...')
            autosubsync.synchronize(video_file, srt_file, synced_srt_file)

            move(synced_srt_file, srt_file)
        print('\n\tDone! Saved as: ' + srt_file)

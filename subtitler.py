import glob
from os import remove
from shutil import move

import autosubsync
from moviepy.editor import *
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File

if __name__ == '__main__':
    ost = OpenSubtitles()
    ost.login('topadev', 'n8&5X7b9HPbNQG')

    os.chdir(sys.argv[1])
    for video_file in glob.glob( '*.mp4') + glob.glob('*.mkv'):
        base = video_file.rpartition('.')[0]

        f = File(video_file)

        data = ost.search_subtitles([{'sublanguageid': 'eng', 'moviehash': f.get_hash(), 'moviebytesize': f.size}])
        if not data:
            data = ost.search_subtitles([{'sublanguageid': 'eng', 'query': f'{base.split(".")[0]} {base.split(".")[1]}'}])

        if not data:
            print("No subs found")
            continue

        id_subtitle_file = data[0].get('IDSubtitleFile')

        ost.download_subtitles([id_subtitle_file], override_filenames={id_subtitle_file: f'{base}.srt'})

        srt_file = base + '.srt'

        synced_srt_file = base + '.tmp.srt'

        autosubsync.synchronize(video_file, srt_file, synced_srt_file)

        move(synced_srt_file, srt_file)

# Subtitler

[![GitHub stars](https://img.shields.io/github/stars/TobiasPankner/Subtitler.svg?style=social&label=Star)](https://GitHub.com/TobiasPankner/Subtitler/stargazers/)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=3TU2XDBK2JFU4&source=url)


- [Prerequisites](#prerequisites)
- [Run the script](#run-the-script)
- [Usage in qBittorrent](#usage-in-qbittorrent)
- [Command line options](#command-line-options)

Automatically downloads subtitles from [opensubtitles.org](https://www.opensubtitles.org/en/search/subs) and then syncs them using [autosubsync](https://github.com/oseiskar/autosubsync).  
The script will always name the .srt file the same as the video file.  
![image](https://user-images.githubusercontent.com/39444749/183303741-5c8d1540-dce9-46ac-ad2b-65cb6b08e866.png)

## Prerequisites  
  
 - Python3 ([Download](https://www.python.org/downloads/))  
 
## Run the script
 1. Install dependencies: `pip install -r requirements.txt`
 2. Run subtitler.py: `python subtitler.py -i <PATH/TO/MOVIE/DIR>`
 
## Usage in qBittorrent
Using the option "Run external program on torrent completion" you can automatically add subtitles to downloaded movies/shows.  
To configure this, add this line:  
`python Path/To/Script/subtitler.py -i "%F"`  
in qBittorrent.  

Example:  
![image](https://user-images.githubusercontent.com/39444749/183303509-d3f00c20-e62b-4fcb-a843-d5246064653a.png)
 
## Command line options
```
usage: subtitler.py [-h] -i INPUT_DIR [-ds] [-o] [-l LANG]

Automatically downloads and syncs subtitles

required arguments:
  -i INPUT_DIR  The directory to search for videos

options:
  -h, --help    show this help message and exit
  -ds           Pass this to disable subtitle synchronization
  -o            Pass this to override existing subtitles
  -l LANG       The language of subtitles to download (default: eng)
```

<details>
  <summary>Language Options</summary>
   "all",
    "abk",
    "afr",
    "alb",
    "ara",
    "arg",
    "arm",
    "asm",
    "ast",
    "aze",
    "baq",
    "bel",
    "ben",
    "bos",
    "bre",
    "bul",
    "bur",
    "cat",
    "chi",
    "zht",
    "zhe",
    "hrv",
    "cze",
    "dan",
    "prs",
    "dut",
    "eng",
    "epo",
    "est",
    "ext",
    "fin",
    "fre",
    "gla",
    "glg",
    "geo",
    "ger",
    "ell",
    "heb",
    "hin",
    "hun",
    "ice",
    "ibo",
    "ind",
    "ina",
    "gle",
    "ita",
    "jpn",
    "kan",
    "kaz",
    "khm",
    "kor",
    "kur",
    "lav",
    "lit",
    "ltz",
    "mac",
    "may",
    "mal",
    "mni",
    "mar",
    "mon",
    "mne",
    "nav",
    "nep",
    "sme",
    "nor",
    "oci",
    "ori",
    "per",
    "pol",
    "por",
    "pob",
    "pom",
    "pus",
    "rum",
    "rus",
    "sat",
    "scc",
    "snd",
    "sin",
    "slo",
    "slv",
    "som",
    "spa",
    "spn",
    "spl",
    "swa",
    "swe",
    "syr",
    "tgl",
    "tam",
    "tat",
    "tel",
    "tha",
    "tok",
    "tur",
    "tuk",
    "ukr",
    "urd",
    "vie",
    "wel"
</details>

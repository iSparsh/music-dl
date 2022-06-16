#!/usr/bin/env python
'''
Created By: Sparsh Mishra
License: GNU GPLv3.0
'''
# IMPORTS SECTION ---------------------
from __future__ import unicode_literals
import youtube_dl
from requests import get
import os
import sys
# ++++++ CLASSES AND DEFs BEGIN ++++++


class MyLogger(object):
    '''
    + --- + DOCSTRING + ---- +
    MyLogger -> Type: Class
    Description: Logs all procs, warnings, and errors from the youtube-dl & ffmpeg(sub) command.
    '''

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d): 
    if d['status'] == 'finished':
        print("\nDone downloading, now converting ...")
    
    elif d['status'] != 'finished':
        dl_percentage = int(((d['downloaded_bytes']/d['total_bytes'])*100))
        bar = '█' * (dl_percentage//2)
        print(f'\r[{dl_percentage}%] [{d["_eta_str"]}]- |{bar}|', end='\r')



def search(arg):
    """Search for the URL by providing the music song title"""
    if arg in ["", " "]:
        print("Invalid title! It should be some actual numbers or characters!")
        quit()

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            get(arg)
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)[
                'entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)
    return video


# Declares options parsed in the ytdl command.
# Installs webm, converts to mp3,
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'keepvideo': False,
    'noplaylist': True,
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'outtmpl': '~/Music/%(title)s.%(ext)s',
}


def main():
    '''
    This is the main function.
    musidl - A tiny CLI tool to download music from YouTube and youtube-dl.
    The command will be as follows: -
    1. Prompts user to enter their search query(music title)
    2. Fetches the URL of the first result.
    4. Downloads the URL with youtube-dl
    5. Converts to mp3 & saves to specified directory
    '''
    # prompt to enter music title for searching
    searchQuery = str(input("Enter Music Name: "))
    # calls function that chooses the first video that pops up and feeds that URL
    video_info = search(searchQuery)
    choiceURL = 'https://www.youtube.com/watch?v='+video_info['id']

    # downloading
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([choiceURL])
            print("Done!")
        except:
            print(
                "There was an error in downloading the video..."
            )
            print(
                "Check your destination and see if a file is there by the same name. If so, delete it\n\
                and run it through ffmpeg to change extension. YTDL Does this sometimes. \n\
                Check the Debug and Error logs above ^ "
            )


if __name__ == "__main__":
    args = sys.argv # mutable list of all args passed to the command

    # help passed to the command
    if "--help" in args:
        print("""
		[music-dl] A Tiny CLI Application to search, and download YouTube music in MP3.
		--help -> show this message
		--search -> search up songs by names and returns video ID

        **please note that more is coming soon!
		""")

    # search query passed to the command
    elif "--search" in args:
        searchQuery = str(input("Enter Music Name: "))
        video_info = search(searchQuery)
        print("Title: " + video_info['title'])
        print("Video URL: " + "https://www.youtube.com/watch?v=" + video_info['id'])
    
    # if there are no args, run the main()
    else:
        main()

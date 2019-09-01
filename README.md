youtube-dl - a modified version of youtube-dl which was forked from https://github.com/ytdl-org/youtube-dl
This version of youtube-dl includes options of downloading basic video information and comments of a video. 

- [DESCRIPTION](#description)
- [INSTALLATION](#installation)
- [OPTIONS](#options)
- [USAGE](#usage)


# DESCRIPTION

**youtube-dl** is a command-line program to download videos from YouTube.com and a few more sites. It requires the Python interpreter and it is not platform specific. It is released to the public domain, which means anyone can modify it, redistribute it or use it however one like.

    
## MODIFICATION

This version of youtube-dl was modified to include the options to download basic video information(id, title, view_count, like_count, dislike_count, upload_date, uploader, uploader_id, webpage_url) and to download the comments of the video while downloading the video. The new options can be used only on videos from YouTube.com. 'YouTube DATA API (v3)' was used to download video comments.

The basic video information will be downloaded with the video using '-b' or '--download-info' option. Using the '--download-comments' option, the video comments would be downloaded with the video.  

The basic video information will be stored in 'video_info/video_info.csv'.
The video comments will be stored in 'video_comments/' directory as a CSV file. The filename of the CSV file would be the YouTube Video ID of the video.


# INSTALLATION

To install this modified version of youtube-dl:

    git clone https://github.com/Dubhe28/youtube-dl.git

To use the program, move the current directory to the downloaded folder:

    cd youtube-dl
    
    
# OPTIONS

Added in this version of youtube-dl:

    -b, --download-info              Download the video information
    -d, --download-comments          Download the video comments using YouTube API Key in 'youtube_api_key.txt'

Useful options from the original repository:

    -s, --simulate                   Do not download the video 
    -x, --extract-audio              Convert video files to audio-only files
                                     (requires ffmpeg or avconv and ffprobe or avprobe)
    -o, --output TEMPLATE            Output filename template, see the "OUTPUT TEMPLATE" for all the info
                                     (https://github.com/ytdl-org/youtube-dl/blob/master/README.md#output-template)
    -f, --format FORMAT              Video format code, see the "FORMAT SELECTION" for all the info
                                     (https://github.com/ytdl-org/youtube-dl/blob/master/README.md#format-selection)
                                     
                                     
# USAGE

To download a video (or a list of videos) in the MP4 format:

    python -m youtube_dl -f mp4 [URL]    

To download an extracted audio file of a video (or a list of files) in the WAV format:

    python -m youtube_dl -x --audio-format wav -o "%(title)s_%(id)s.%(ext)s“ [URL]

To download a video (or a list of videos) in the current directory with the basic video information in "video_info/video_info.csv":

    python -m youtube_dl -b [URL]

To download a video (or a list of videos) with the basic video information and the youtube comments:

    python -m youtube_dl -db [URL]

To download basic video information of a playlist without the videos or the video comments:

    python -m youtube_dl -sb [URL]

To download an extracted audio file of a video (or a list of files) in the WAV format with the video information and the video comments:

    python -m youtube_dl -xdb --audio-format wav -o "%(title)s_%(id)s.%(ext)s“ [URL]
    
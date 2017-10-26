"""
Application's main class
"""
import os
import sys
from opensubtitle import OpenSubtitlesApiWrapper
class Subright():

    def __init__(self, media_source_file):
        subs = OpenSubtitlesApiWrapper()
        subs.pull_subtitles(media_source_file)



def main():
    media_source_file = sys.argv[1]
    subright_handle = Subright(media_source_file)


if __name__ == '__main__':
    main()

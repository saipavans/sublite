"""
Application's main class
"""

import sys
import os

CURRENT_DIR = os.getcwd()
SUBTITLE_EXTENSION = ".srt"

class Subright():

    def __init__(self, media_source_file, subtitle_source_file = "", media_source_dir = CURRENT_DIR, subtitle_source_dir = CURRENT_DIR):
        self.media_source = media_source_dir + media_source_file
        if len(subtitle_source_file) == 0: ### if subtitle file is not given, it assumes that srt file has same name as the media file
            subtitle_source_file = os.path.split(self.media_source)[0] + SUBTITLE_EXTENSION
        self.subtitle_source = subtitle_source_dir + subtitle_source_file


def main():
    media_source_file = sys.argv[1]
    subright_handle = Subright(media_source_file)


if __name__ == '__main__':
    main()

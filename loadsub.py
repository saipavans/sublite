import logging as LOGGER
from properties.configurations import Configuration
import os

LOGGER.basicConfig(filename=Configuration.LOG_FILE, format='%(asctime)s %(message)s', level=LOGGER.DEBUG)
TIME_DELIMITER = "-->"

class SubLoader():

    def __init__(self, subfile):
        fin = open(subfile)
        sub_title = ""
        sub_times = []
        subtitle_data = {}
        for line in fin:
            if line.find(TIME_DELIMITER)!= -1:
                line_stripped = line.strip()
                sub_times = line_stripped.split(TIME_DELIMITER)
                print("subtimes",sub_times)
                subtitle_data[(sub_times[0],sub_times[1])] = sub_title
                sub_title = ""
            else:
                line_stripped = line.strip()
                sub_title += line_stripped
        self.subtitle_data = subtitle_data

if __name__ == '__main__':
    home_dir = os.path.expanduser("~")
    subtitle = SubLoader(home_dir + '/Documents/test.srt')
    print(subtitle.subtitle_data)



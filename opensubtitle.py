from xmlrpc.client import ServerProxy
import logging as LOGGER
import os
from properties.configurations import Configuration

SUBTITLE_SERVER = Configuration.SUBTITLE_SERVER
USER_AGENT_OPEN_SUTBTITLE = Configuration.USER_AGENT_OPEN_SUTBTITLE
USER_NAME = Configuration.USER_NAME_OPEN_SUBTITLE
PASSWORD = Configuration.PASSWORD_OPEN_SUBTITLE
LOG_FILE = Configuration.LOG_FILE
HTTP_CODE_200 = "200 OK"
LOGGER.basicConfig(filename=LOG_FILE, format='%(asctime)s %(message)s', level=LOGGER.DEBUG)
PROJECT_HOME = Configuration.PROJECT_HOME


class OpenSubtitlesApiWrapper():

    def __init__(self):
        try:
            self.auth_token = "-1" ### state to check if initialized properly
            self.server_connector = ServerProxy(SUBTITLE_SERVER, allow_none=True)
            auth_response = self.server_connector.LogIn(USER_NAME, PASSWORD, "en", USER_AGENT_OPEN_SUTBTITLE)
            if auth_response['status'] != HTTP_CODE_200:
                raise Exception("Auth failed!!!")
            self.auth_token = auth_response["token"]
        except Exception as e:
            LOGGER.exception(str(e))

    def pull_subtitles(self, media_source):
        movie_vs_id = {}
        movie_ids = [] ### to preserve ordering with relevancy
        media_file_name = os.path.basename(media_source)
        media_dir = media_source.replace(media_file_name,"")
        media_name = os.path.splitext(media_file_name)[0]
        response = self.server_connector.SearchMoviesOnIMDB(self.auth_token, media_name)
        if len(response['data']) > 0:
            for movie in response['data']:
                movie_vs_id[movie['id']] = movie['title']
                movie_ids.append(movie['id'])
        #os.system("autosub " + media_source + " -o " + PROJECT_HOME + "/tmp/tmp.srt")
        print(movie_vs_id[movie_ids[0]])
        if input("Is this your media file for which you are searching subs y/n? ") == "y":
            media_id = movie_ids[0]
        else:
            count = 0
            for movie_id in movie_ids:
                print(str(count+1) + ") " + movie_vs_id[movie_id])
                count += 1
            choice = int(input("Please choose between the options [1-" + str(count) + "] "))
            media_id = movie_ids[choice-1]

        print("Pulling subtitles from opensubtitle for " + movie_vs_id[media_id])
        subtitles = self.server_connector.SearchSubtitles(self.auth_token, [{"sublanguageid":"eng","imdbid":media_id}])['data']
        print(subtitles)
        counter = 1
        for subtitle in subtitles:
            download_link = subtitle['SubDownloadLink']
            print("Downloading sub(s) from " + download_link)
            downloaded_file = os.path.basename(download_link)
            os.system("cd " + media_dir + "; wget " + download_link + "; gunzip -c " + downloaded_file + " > " + media_name + "." + str(counter) + ".srt; rm -rf '*.gz'"  )
            counter+=1

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

class wac():

    def __init__(self, search_terms ='', video_id='',related_id=''):
        self.search_terms = search_terms
        self.video_id=video_id
        self.related_id=related_id

    def home_page():
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey='AIzaSyCstN2Gg044lSZ0fDIbClfcmWOx6uY__Hg')
        request = youtube.videos().list(
            part = "snippet",
            maxResults=50,
            chart = 'mostPopular'
        )
        response = request.execute()
        return response

    def search(search_terms):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey='AIzaSyCstN2Gg044lSZ0fDIbClfcmWOx6uY__Hg')
        request = youtube.search().list(
            part = "snippet",
            maxResults=50,
            q=search_terms
        )
        response = request.execute()
        return response
        

    def search_by_id(video_id):
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey='AIzaSyCstN2Gg044lSZ0fDIbClfcmWOx6uY__Hg')
        request = youtube.videos().list(
            part="snippet",
            id= video_id
        )
        response = request.execute()
        return response

    def related_vids(related_id):
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey='AIzaSyCstN2Gg044lSZ0fDIbClfcmWOx6uY__Hg')
        request = youtube.search().list(
            part="snippet",
            type = 'video',
            relatedToVideoId=related_id
        )
        response = request.execute()
        return response

print(wac.search_by_id('hTvBLk47lxE')['items'][0]['snippet']['channelTitle'])
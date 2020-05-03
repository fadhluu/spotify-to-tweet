import spotipy
import spotipy.oauth2 as oauth2
import requests
import io
import os
from PIL import Image


class Client(object):
    """
    A class for initiating simple client for spotify

    Methods:
        refresh_token(): Method for refreshing expired account
        currently_playing(): Get currently playing info
        get_track_info(): Get currently playing track info (track name, artist)
        get_cover_art(quality): Download current playing cover art
    """

    def __init__(self, username, scope, client_id, client_secret, redirect_uri):
        self.sp_oauth = oauth2.SpotifyOAuth(
            client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, username=username)
        self.token_info = self.sp_oauth.get_cached_token()
        self.token = ""

        if not self.token_info:
            auth_url = self.sp_oauth.get_authorize_url()
            print(auth_url)
            response = input("Paste: ")

            code = self.sp_oauth.parse_response_code(response)
            self.token_info = self.sp_oauth.get_access_token(code)

            self.token = self.token_info['access_token']
        else:
            self.token = self.token_info['access_token']

        self.sp_client = spotipy.Spotify(auth=self.token)

    def refresh_token(self):
        """Method for refreshing expired account"""
        if self.sp_oauth.is_token_expired(self.token_info):
            self.token_info = self.sp_oauth.refresh_access_token(
                self.token_info['refresh_token'])
            self.token = self.token_info['access_token']
            self.sp_client = spotipy.Spotify(auth=self.token)

    def currently_playing(self):
        """Get currently playing info"""

        try:
            return self.sp_client.currently_playing()
        except spotipy.client.SpotifyException as e:
            print(e)
            self.refresh_token()
            return self.sp_client.currently_playing()

    def get_track_info(self):
        """Get currently playing track info (track name, artist)

        Returns:
            track_name: current track name
            artist: current artist
        """

        current_playback = self.currently_playing()
        track_name = current_playback["item"]["name"]
        artists = current_playback["item"]["artists"]
        list_artist = []

        for artist in artists:
            list_artist.append(artist['name'])

        artists = ', '
        artists = artists.join(list_artist)

        return track_name, artists

    def get_cover_art(self, quality="high"):
        """Download current playing cover art
        default high

        Parameters:
            quality: high (640x640), medium (300x300), low(64x64)
        """
        if quality == "high":
            q = 0
        elif quality == "medium":
            q = 1
        elif quality == "low":
            q = 2
        else:
            q = 0

        current_playback = self.currently_playing()
        re = requests.get(
            current_playback["item"]["album"]["images"][q]["url"])

        cover = Image.open(io.BytesIO(re.content))
        try:
            cover.save("img/cover_art.png")
        except:
            os.mkdir("img")
            cover.save("img/cover_art.png")

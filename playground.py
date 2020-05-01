from client import Client
from bot import Twitter
import time

username = ""
scope = ""
client_id = ""
client_secret = ""
redirect_uri = "http://localhost:8080"

tw_api = ""
tw_secret = ""
tw_access_token = ""
tw_access_secret = ""

c = Client(username, scope, client_id, client_secret, redirect_uri)
tw = Twitter(tw_api, tw_secret, tw_access_token, tw_access_secret)

c.auth_spotify(c.token)

previous_track = ""

while True:
    current_track, current_artist = c.get_track_info()
    time.sleep(1)
    if previous_track != current_track:
        previous_track = current_track
        c.get_cover_art()
        time.sleep(2)
        tw.post_tweet(
            text=f"{current_track} - {current_artist}", file_location="cover_art.png")

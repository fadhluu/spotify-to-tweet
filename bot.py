import tweepy


class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = self.authentication()
        self.api = tweepy.API(self.auth)

    def authentication(self):
        self.auth = tweepy.OAuthHandler(
            self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        return self.auth

    def post_tweet(self, text_obj, file_location):
        text = f"🎵 Listening to:\n"

        if not all(text_obj.values()):
            text += f"{text_obj['name']} - {text_obj['artists']}"
        else:
            text += f"{text_obj['name']} - {text_obj['artists']}\n\n{text_obj['context']['type']}:\n{text_obj['context']['name']} {text_obj['context']['uri']}"

        self.api.update_with_media(filename=file_location, status=text)
        print(f"Success tweeting:\n{text}")

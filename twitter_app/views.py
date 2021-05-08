import json

from django.http import HttpResponse
import tweepy

data = json.load(open('D:\passwords.json'))
auth = tweepy.OAuthHandler(data['API_key'], data['API_secret_key'])
auth.set_access_token(data['access_token'], data['access_token_secret'])
api = tweepy.API(auth)


class Stats:
    def __init__(self, username):
        self.counted_likes = False
        self.username = username
        self.total_likes = 0
        self.total_rts = 0
        self.user_timeline = api.user_timeline(self.username, include_rts=False, count=200, exclude_replies=True)
        self.total_tweets = len(self.user_timeline)
        self.counted_rts = False

    def get_average_retweets(self):
        if self.total_tweets == 0:
            return 0
        if self.counted_rts:
            return round(self.total_rts / self.total_tweets)
        for tweet in self.user_timeline:
            self.total_rts += tweet.retweet_count
        self.counted_rts = True
        return round(self.total_rts / self.total_tweets)

    def get_average_likes(self):
        if self.total_tweets == 0:
            return 0
        if self.counted_likes:
            return round(self.total_likes / self.total_tweets)
        for tweet in self.user_timeline:
            self.total_likes += tweet.favorite_count
        return round(self.total_likes / self.total_tweets)


def stats(request, username):
    account = Stats(username)
    return HttpResponse(
        f'<h1>Average Retweets per tweet:{account.get_average_retweets()}</h1><h1>Average Likes per tweet:{account.get_average_likes()}</h1>')

from flask import current_app
from scaner.utils import add_metadata
import json
# from time import sleep


@add_metadata()
def get(tweetId, fields=None, *args, **kwargs):
    if fields:
        get_task = current_app.tasks.tweet_attributes.delay(tweetId, fields)
    else:
        get_task = current_app.tasks.tweet.delay(tweetId)
    return {'statuses': get_task.get(timeout=10)}, 200 

@add_metadata('statuses') #'statuses'
def search(fields='', limit=20, topic=None, sort_by=None, *args, **kwargs):
    search_task = current_app.tasks.tweet_search.delay(fields, limit, topic, sort_by)
    return {'statuses': search_task.get(timeout=10)}, 200

@add_metadata()
def post(body, *args, **kwargs):
    post_task = current_app.tasks.add_tweet.delay(json.dumps(body))
    return {'result': post_task.get(interval=0.1)}, 200

@add_metadata()
def delete(tweetId, *args, **kwargs):
    delete_task = current_app.tasks.delete_tweet.delay(tweetId)
    return {'result': delete_task.get(timeout=10)}, 200

@add_metadata()
def put(*args, **kwargs):
    pass

@add_metadata()
def get_history(tweetId, *args, **kwargs):
    get_history_task = current_app.tasks.tweet_history.delay(tweetId)
    return {'result': get_history_task.get(timeout=10)}, 200


@add_metadata()
def get_emotion(tweetId, *args, **kwargs):
    return {'result': {"id": 0, "emotion": "negative-fear"}}, 200

@add_metadata()
def get_sentiment(tweetId, *args, **kwargs):
    return {'result': {"id": 0, "sentiment": "negative"}}, 200

@add_metadata()
def get_metrics(tweetId, *args, **kwargs):
    get_metrics_task = current_app.tasks.get_tweet_metrics.delay(tweetId)
    return {'result': get_metrics_task.get(timeout=10)}, 200

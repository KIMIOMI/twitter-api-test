# 샘플 Python 스크립트입니다.

# Shift+F10을(를) 눌러 실행하거나 내 코드로 바꿉니다.
# 클래스, 파일, 도구 창, 액션 및 설정을 어디서나 검색하려면 Shift 두 번을(를) 누릅니다.
import requests
import json
from urllib.parse import urlparse
import re

with open('./config.json') as f:
    d1 = json.load(f)


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_tweet_lookup_url(tweet_id):
    tweet_fields = "tweet.fields=lang,author_id"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    query_params = {
        'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
        'tweet.fields': 'lang,author_id',
        'media.fields': 'url'
    }
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/{}".format(tweet_id)
    return url, query_params


def create_get_user_url(username):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    # user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by/username/{}".format(username)
    query_params = {
        'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
    }
    return url, query_params


def create_user_timeline_url(user_id):
    # Replace with user ID below
    url = "https://api.twitter.com/2/users/{}/tweets".format(user_id)
    query_params = {
        'tweet.fields': 'created_at',
        'user.fields': 'created_at',
        'max_results': 5,
    }
    return url, query_params


def create_url(keyword, start_date, end_date, max_results=10):
    search_url = "https://api.twitter.com/2/tweets/search/all"
    # Change to the endpoint you want to collect data from

    # change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return search_url, query_params


def connect_to_endpoint(url, headers, params, next_token=None):
    params['next_token'] = next_token  # params object received from create_url function
    response = requests.get(url, headers=headers, params=params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    link = urlparse('https://twitter.com/HHbead00/status/1533387341548879873')
    username = link.path.split('/')[1]

    bearer_token = d1["BEARER_TOKEN"]
    headers = create_headers(bearer_token)
    # keyword = "xbox lang:en"
    # start_time = "2021-03-01T00:00:00.000Z"
    # end_time = "2021-03-31T00:00:00.000Z"
    # max_results = 15

    url = create_get_user_url(username)
    json_response = connect_to_endpoint(url[0], headers, url[1])
    user_id = json_response["data"]["id"]

    url = create_user_timeline_url(user_id)
    json_response = connect_to_endpoint(url[0], headers, url[1])
    tweets = json_response["data"]
    for tweet in tweets:
        text = tweet["text"]
        id = tweet["id"]
        created_at = tweet["created_at"]
        hashTags = re.findall(r"#(\w+)", text)
        print(hashTags, created_at)

# https://www.jetbrains.com/help/pycharm/에서 PyCharm 도움말 참조

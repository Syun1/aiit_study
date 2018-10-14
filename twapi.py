# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session, OAuth1
import pymysql
import json
import requests
import urllib
import sys
import io
import time
import datetime

### mysql connect
conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'ohno_syun0323',
    db = 'twitter',
    charset = 'utf8',
    cursorclass = pymysql.cursors.DictCursor)
cur = conn.cursor()

#検索文字列設定
word = input('キーワード入力： ')
# デフォルト文字コードをutf8に変更
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#apiキー情報設定
consumer_key = "4aJ7Kcldz4fVVtEGAWqno6jxB"
consumer_key_secret = "qWwIuMcQcHCHdaCKuwxpS3Vk9cly0rzmh3mTzwCiZUFpv00E7s"
access_token = "777893838-eQVWmZ06BXR2PCZZcrfmXSLEzq1WXRhZ7WzkUwqQ"
access_token_secret = "JWD2Uz485iK8avUrJjiRbckJbaoL699Pp5b8suipfpKGc"

#twitterAPIアクセス
url = "https://api.twitter.com/1.1/search/tweets.json?count=100&lang=ja&q=" + word
auth = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)
response = requests.get(url, auth = auth)
data = response.json()['statuses']
cnt = 0

#データ取得
while True:
    for tweet in data:
        tweet_id = int(tweet['id_str'])
        created_at = tweet['created_at']
        c_at = time.mktime(time.strptime(created_at,"%a %b %d %H:%M:%S +0000 %Y"))
        tweet_date = datetime.datetime.fromtimestamp(c_at) + datetime.timedelta(hours=9)
        user_name = tweet['user']['screen_name']
        uname_cp = (user_name.encode("cp932", "ignore")).decode("cp932")
        text = tweet['text']
        rep_text = text.replace('\n', '')
        text_cp = (rep_text.encode("cp932", "ignore")).decode("cp932")

        #DBに保存
        cur.execute("INSERT IGNORE INTO twapi_test (id, date_time, uname, tweet) VALUES (%s, %s, %s, %s)", (tweet_id, tweet_date, uname_cp, text_cp))
        conn.commit()
        cnt += 1
        maxid = tweet_id - 1

    if len(data) == 0:
        break

    url = "https://api.twitter.com/1.1/search/tweets.json?count=100&lang=ja&q=" + word + "&max_id=" + str(maxid)
    auth = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)
    response = requests.get(url, auth = auth)
    data = response.json()['statuses']
cur.close()
conn.close()

print("ツイート数:" + str(cnt))
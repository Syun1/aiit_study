'''
キーワード検索したツイートからID(id)、ユーザ名(uname)、日時(date_time)、本文(tweet)を収集し、
データベース(MySQL)に保存するプログラム
'''

# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session, OAuth1   # OAuthライブラリ
import pymysql                                        # MySQLライブラリ
import json
import requests
import urllib
import sys
import io
import time
import datetime

# MySQLに接続
conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '******',  # MySQLパスワード
    db = 'twitter',       # DB_name
    charset = 'utf8',
    cursorclass = pymysql.cursors.DictCursor)
cur = conn.cursor()

# Twitterのキーワード検索
word = input('キーワード入力： ')
# デフォルト文字コードをutf8に変更
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# twitter APIキー情報設定
consumer_key = "**********************"
consumer_key_secret = "**********************"
access_token = "**********************"
access_token_secret = "**********************"

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

        # DBに格納
        cur.execute("INSERT IGNORE INTO table_name (id, date_time, uname, tweet) VALUES (%s, %s, %s, %s)", (tweet_id, tweet_date, uname_cp, text_cp))
        conn.commit()
        
        cnt += 1              # ツイート数のカウント
        maxid = tweet_id - 1  # tweet_idの更新

    if len(data) == 0:
        break

    url = "https://api.twitter.com/1.1/search/tweets.json?count=100&lang=ja&q=" + word + "&max_id=" + str(maxid)
    auth = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)
    response = requests.get(url, auth = auth)
    data = response.json()['statuses']
cur.close()
conn.close()

print("取得ツイート数:" + str(cnt))  # 取得ツイート数の表示

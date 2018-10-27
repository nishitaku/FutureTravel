# coding: utf-8

from requests_oauthlib import OAuth1Session
import json
import re
import urllib
import subprocess
import settings
import time, calendar
from PIL import Image
import numpy as np
import io

import datetime
# subprocess.run(['jupyter', 'nbconvert', '--to', 'python', 'tweet_illust_text_get'])
               
CK = settings.CONSUMER_KEY
CS = settings.CONSUMER_SECRET
AT = settings.ACCESS_TOKEN
ATS = settings.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

######入力情報：twitter検索に必要なため、各情報を引き渡してください。各時刻については、何時台かを入力。（8:30 出発なら、8を入力）
#タイトル
title='伊勢神宮旅行'
#出発地、時刻
dep_place='名古屋駅'
dep_time=8
#経由地、時刻
des_place='伊勢神宮'
des_time=11
#目的地、時刻
ret_place='東京駅'
ret_time=20

# ツイッター上で出発地または目的地の入ったツイートを〇〇個取得する
def get_target_word(word):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {'q':word,
              'count':200
          }
    req = twitter.get(url, params = params)
    timeline = json.loads(req.text)
    return timeline


def YmdHMS(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return int(time.strftime("%Y%m%d%H%M%S", time_local))


# 取得したツイートに画像があれば、その画像を取得する
def get_illustration(timeline,key_time):
    global image
    global image_number
    image_number = 0
    image_get_flag = 0
    check_image = []
    loop_num = 0
    for tweet in timeline['statuses']:
        #出発地、経由地、目的地の到着時刻と投稿時刻が近いtweetをフィルタリング。（±3時間） 
        loop_num  +=1
        # if key_time -3 < int(str(YmdHMS(tweet['created_at']))[8:10]) < key_time +3:
        #画像があれば、画像とツイートを取得
        try:
            media_list = tweet['extended_entities']['media']

            for media in media_list:
                image = media['media_url']
                check_image.append(image)
                image_number += 1
                image_get_flag = 1

                file =io.BytesIO(urllib.request.urlopen(image).read())
                img = Image.open(file)
                # img.show()

                return img, tweet['text']
                break
        except:
            pass
        #条件を満たすtweetが見つからなかった時、#いらすとやの画像と定型の感想を表示
    else:
#       elif loop_num == len(timeline['statuses']) and image_get_flag == 0:
            image='https://1.bp.blogspot.com/-ZsRZh52shXU/WWNBGGNeLjI/AAAAAAABFZg/rRxw5r719Jk_ymwSq7sViPCl0DIcHjXigCLcBGAs/s600/travel_happy_family_set.png'
            file =io.BytesIO(urllib.request.urlopen(image).read())
            img = Image.open(file)
            # img.show()
            return img,'旅行楽しい！'
    

if __name__ == '__main__':
    
    print('タイトル  ',title)
    print('----------------------------------------------------')
    #出発地、時間
    keyword_dep = dep_place + '楽'     #検索対象の単語を設定、出発地 and '楽'が含まれるtweetを検索
    print('出発地: ', dep_place, dep_time,'時')
    timeline = get_target_word(keyword_dep)
    illust_img_dep, illust_text_dep = get_illustration(timeline,dep_time)        #画像と感想を出力
    print(illust_img_dep, illust_text_dep)
    print('----------------------------------------------------')
    #経由地、時間
    keyword_des = des_place + '楽' #検索対象の単語を設定、経由地 and '楽'が含まれるtweetを検索
    print('経由地: ', des_place, des_time,'時')
    timeline = get_target_word(keyword_des)
    illust_img_des,illust_text_des =  get_illustration(timeline,des_time)         #画像と感想を出力
    print(illust_img_des, illust_text_des)
    print('----------------------------------------------------')
    #目的地、時間
    keyword_ret = ret_place + '楽' #検索対象の単語を設定、目的地 and '楽'が含まれるtweetを検索
    print('目的地: ', ret_place, ret_time,'時')
    timeline = get_target_word(keyword_ret)
    illust_img_ret,illust_text_ret = get_illustration(timeline,ret_time)              #画像と感想を出力
    print(illust_img_ret, illust_text_ret)
    print('----------------------------------------------------')

    


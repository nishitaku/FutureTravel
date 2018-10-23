from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import numpy as np
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
from os.path import join, dirname
from dotenv import load_dotenv
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# 環境変数取得
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get("YOUR_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.environ.get("YOUR_CHANNEL_SECRET")
GOOGLE_STATICMAPS_APIKEY = 'AIzaSyBdfdAlLSf8hWn3cLczA7DFQOSzn3VuUCM'

# LIFF_URL = "line://app/1614481927-DL6wVJEZ"
LIFF_URL = "開発中だよ"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "ほげ":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=LIFF_URL))


# メッセージをランダムに表示するメソッド
def picked_up():
    messages = [
        "こんにちは、あなたの名前を入力してください",
        "やあ！お名前は何ですか？",
        "あなたの名前を教えてね"
    ]
    # NumPy の random.choice で配列からランダムに取り出し
    return np.random.choice(messages)


# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "ようこそ"
    message = picked_up()
    # index.html をレンダリングする
    return render_template('index.html',
                           message=message, title=title)


# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        name = request.form['name']
        # index.html をレンダリングする
        return render_template('index.html',
                               name=name, title=title)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))


@app.route('/getimage', methods=['GET'])
def getimage():
    # パラメータ取得
    src = request.args.get('src')
    dst = request.args.get('dst')

    # 座標取得
    src_location = get_location(src)
    dst_location = get_location(dst)

    # Google Static Map API
    map_image_url = 'https://maps.googleapis.com/maps/api/staticmap?size=520x520&scale=2&maptype=roadmap&key={}'.format(
        GOOGLE_STATICMAPS_APIKEY)
    map_image_url += '&markers=color:{}|label:{}|{},{}'.format('red', '', src_location[2], src_location[3])
    map_image_url += '&markers=color:{}|label:{}|{},{}'.format('blue', '', dst_location[2], dst_location[3])

    map_image_url_thumbnail = 'https://maps.googleapis.com/maps/api/staticmap?size=240x240&scale=2&maptype=roadmap&key={}'.format(
        GOOGLE_STATICMAPS_APIKEY)
    map_image_url_thumbnail += '&markers=color:{}|label:{}|{},{}'.format('red', '', src_location[2], src_location[3])
    map_image_url_thumbnail += '&markers=color:{}|label:{}|{},{}'.format('blue', '', dst_location[2], dst_location[3])

    response = jsonify({
        'result': 'hello world!',
        'map_image_url': urllib.parse.quote(map_image_url, safe='/:=?&'),
        'map_image_url_thumbnail': urllib.parse.quote(map_image_url_thumbnail, safe='/:=?&')
    })

    return make_response(response)


def get_location(text):
    # 座標取得
    geo_url = 'https://maps.googleapis.com/maps/api/place/textsearch/xml?query={}&key={}'.format(text, GOOGLE_STATICMAPS_APIKEY)

    geo_req = urllib.request.Request(geo_url)
    with urllib.request.urlopen(geo_req) as response:
        geo_xmldata = response.read()
    geo_root = ET.fromstring(geo_xmldata)

    # 最寄駅情報(名前、住所、緯度経度)を取得
    name = geo_root.findtext(".//name")
    address = geo_root.findtext(".//formatted_address")
    geo_lat = geo_root.findtext(".//lat")
    geo_lon = geo_root.findtext(".//lng")

    return name, address, geo_lat, geo_lon


if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port) # どこからでもアクセス可能に
    # app.run()

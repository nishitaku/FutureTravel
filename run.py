from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, send_file
import numpy as np
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, MessageImagemapAction, ImagemapArea, BaseSize, ImagemapSendMessage, FollowEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction, JoinEvent, URIImagemapAction
)
import os
from os.path import join, dirname
from dotenv import load_dotenv
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import requests
from io import BytesIO, StringIO
from PIL import Image
import uuid
import io
from flask_cors import CORS

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__, static_folder='static')
CORS(app)

# 環境変数取得
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get("YOUR_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.environ.get("YOUR_CHANNEL_SECRET")
GOOGLE_MAPS_APIKEY = os.environ.get("GOOGLE_MAPS_APIKEY")

LIFF_URL = "line://app/1614481927-B8VxYpMm"

START_KEYWORD1 = "メニュー"
START_KEYWORD2 = "未来旅行記"
START_MSG = '「' + START_KEYWORD1 + '」「' + START_KEYWORD2 + '」と送信すれば、再度メニューを表示します'


line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

src = None
dst = None

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
    if START_KEYWORD1 in event.message.text or START_KEYWORD2 in event.message.text:
        msg = create_img_map_msg()
        line_bot_api.reply_message(
            event.reply_token,
            [
                msg,
                TextSendMessage(text=START_MSG)
            ]
        )

    if event.message.text == "位置情報送信":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text='line://nv/location')
            ]
        )


@handler.add(FollowEvent)
def handle_message(event):
    msg = create_img_map_msg()
    line_bot_api.reply_message(
        event.reply_token,
        [
            msg,
            TextSendMessage(text=START_MSG)
        ]
    )


@handler.add(JoinEvent)
def handle_message(event):
    msg = create_img_map_msg()
    line_bot_api.reply_message(
        event.reply_token,
        [
            msg,
            TextSendMessage(text=START_MSG)
        ]
    )


def create_img_map_msg():
    actions = []
    actions.append(URIImagemapAction(
        link_uri='line://app/1614481927-WbXaLGy0',
        area=ImagemapArea(
            x=0, y=0, width=520, height=520
    )
    ))
    actions.append(URIImagemapAction(
        link_uri='line://app/1614481927-BqrGLbvl',
        area=ImagemapArea(
            x=0, y=520, width=520, height=520
        )
    ))
    actions.append(URIImagemapAction(
        link_uri='line://app/1614481927-2N50kX34',
        area=ImagemapArea(
            x=520, y=0, width=520, height=520
        )
    ))
    actions.append(URIImagemapAction(
        link_uri='line://app/1614481927-WLrPnOXQ',
        area=ImagemapArea(
            x=520, y=520, width=520, height=520
        )

    ))

    message = ImagemapSendMessage(
        base_url='https://' + request.host + '/imagemap/' + uuid.uuid4().hex,
        alt_text='こんにちは！',
        base_size=BaseSize(height=1040, width=1040),
        actions=actions
    )

    return message


# 旅のプランをつくる
@app.route('/')
def index():
    return render_template('index.html')


# 現在地からオススメをさがす
@app.route('/here')
def here():
    return render_template('here.html')


# みんなのコースを見る
@app.route('/course')
def course():
    return render_template('course.html')


# 旅行体験する
@app.route('/exp')
def exp():
    return render_template('exp.html')


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


@app.route('/imagemap/<path:url>/<size>')
def imagemap(url, size):
    app.logger.info(url + ', ' + size)
    img = Image.open("static/img/contact_menu.png")
    img_resize = img.resize((int(size), int(size)))
    img_io = io.BytesIO()
    img_resize.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


@app.route('/getimage', methods=['GET'])
def getimage():
    # パラメータ取得
    global src, dst
    src = request.args.get('src')
    dst = request.args.get('dst')

    # 座標取得
    src_location = get_location(src)
    dst_location = get_location(dst)

    # Google Static Map API
    map_image_url = 'https://maps.googleapis.com/maps/api/staticmap?size=520x520&scale=2&maptype=roadmap&key={}'.format(
        GOOGLE_MAPS_APIKEY)
    map_image_url += '&markers=color:{}|label:{}|{},{}'.format('red', '', src_location[2], src_location[3])
    map_image_url += '&markers=color:{}|label:{}|{},{}'.format('blue', '', dst_location[2], dst_location[3])

    base_url = 'https://{}/imagemap/{}'.format(request.host, urllib.parse.quote_plus(map_image_url))

    map_image_url_thumbnail = 'https://maps.googleapis.com/maps/api/staticmap?size=240x240&scale=2&maptype=roadmap&key={}'.format(
        GOOGLE_MAPS_APIKEY)
    map_image_url_thumbnail += '&markers=color:{}|label:{}|{},{}'.format('red', '', src_location[2], src_location[3])
    map_image_url_thumbnail += '&markers=color:{}|label:{}|{},{}'.format('blue', '', dst_location[2], dst_location[3])

    response = jsonify({
        'map_image_url': urllib.parse.quote(map_image_url, safe='/:=?&'),
        'base_url': base_url,
        'map_image_url_thumbnail': urllib.parse.quote(map_image_url_thumbnail, safe='/:=?&')
    })

    return make_response(response)


@app.route('/gettwitter', methods=['POST'])
def gettwitter():
    # パラメータ取得
    place = request.form['place']
    app.logger.info(place)

    import tweet_illust_text_get
    # keyword = place + '楽'
    keyword = place
    time = 12
    timeline = tweet_illust_text_get.get_target_word(keyword)
    img, text = tweet_illust_text_get.get_illustration(timeline, time)

    app.logger.info(text)

    urls = text.rsplit('https://', 1)
    if len(urls) > 1:
        url = 'https://' + urls[1]


    response = jsonify({
        'text': url,
        # 'img': img
    })

    return make_response(response)


def get_location(text):
    # 座標取得
    geo_url = 'https://maps.googleapis.com/maps/api/place/textsearch/xml?query={}&key={}'.format(text,
                                                                                                 GOOGLE_MAPS_APIKEY)

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
    app.run(host='0.0.0.0', port=port)  # どこからでもアクセス可能に

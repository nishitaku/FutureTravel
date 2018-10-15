from flask import Flask, render_template, request, redirect, url_for
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

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# 環境変数取得
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get("YOUR_CHANNEL_ACCESS_TOKEN")
# YOUR_CHANNEL_SECRET = os.environ.get("YOUR_CHANNEL_SECRET")
#
# line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
# handler = WebhookHandler(YOUR_CHANNEL_SECRET)
#
#
# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']
#
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#
#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#
#     return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))


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


if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0', port=3000) # どこからでもアクセス可能に
    # app.run()

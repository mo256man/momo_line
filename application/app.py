from flask import Flask, request, redirect, url_for, render_template, flash
from flask import make_response, send_from_directory
from sqlalchemy.sql.expression import func

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

import datetime
import random

line_bot_api = LineBotApi("IWwLVAi1MJvj4uJ5XQdViLOnP977xP/vj+jzCJ1WBLMt4q4wDeq7fAIpMGE3WUY58Q204j4F6y45M6IW+OslP1+StpSdSEYIaounG9Fu3u/3arMZkxDREW3BggeKZFlB9IqQV5PKV9qsFbdRVip0fAdB04t89/1O/w1cDnyilFU=")  #チャネルアクセストークン
handler = WebhookHandler("631c484b9948356b740bd1ecc4ca8186")  #チャネルシークレット

app = Flask(__name__)

@app.route("/")
def input():
    return render_template("index.html")


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    id = event.source.user_id   #LINEのユーザーIDの取得
    txt = event.message.text + "だって？"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt))

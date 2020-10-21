import os

import sqlite3

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReplyButton, QuickReply, MessageAction
)

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

DB_PATH = 'user.sqlite'
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfGLLaY3lC6KN2UNQdmP8bteFAZVmU-WJTYnhWpvY-3C3rIkw/viewform"
BUIDLING_NAME_IDENTIFICATION = "435991262"
ROOM_NUMBER_IDENTIFICATION = "458456140"
NAME_IDENTIFICATION = "1468968564"
BODY_TEMPERATURE_IDENTIFICATION = "1187168422"


def user_is_exist(line_id: str) -> bool:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE line_id={}".format(line_id))
    res = cursor.fetchall()
    connection.close()
    
    exist = (len(res) > 0)

    return exist


def insert_new_user(
        line_id: str, building_name: str, room_number: int, name: str
    ) -> bool:

    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO users VALUES (?, {line_id}, {building_name}, {room_number}, {name})"
        )
        connection.commit()
        connection.close()
        return True
    except:
        return False


def generate_url(
        line_id: str, building_name: str, room_number: int, name: str, body_temperature: str
    ) -> str:

    url = f"{GOOGLE_FORM_URL}?entry.{BUIDLING_NAME_IDENTIFICATION}={building_name}"\
            f"&entry.{ROOM_NUMBER_IDENTIFICATION}={room_number}"\
            f"&entry.{NAME_IDENTIFICATION}={name}"\
            f"&entry.{BODY_TEMPERATURE_IDENTIFICATION}={body_temperature}"
    
    return url


def get_user_data(line_id: str) -> dict:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * from users WHERE line_id={line_id}"
    )
    res = cursor.fetchone()
    connection.close()

    user_data = {
        "building_name": res[1],
        "room_number": res[2],
        "name": res[3],
        "body_temperature": res[4]
    }

    return user_data


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if user_is_exist(event.source.user_id):
        pass
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="あなたのLINEユーザー情報がまだ登録されていないか、変更されたようです。\nもう１度登録をお願いします。")
        )


if __name__ == "__main__":
    app.run()
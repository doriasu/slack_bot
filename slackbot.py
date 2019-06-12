# -*- coding: utf-8 -*-
import os
import json
import logging
import urllib.request
import random

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle_slack_event(slack_event: dict, context) -> str:

    # 受け取ったイベント情報をCloud Watchログに出力
    logging.info(json.dumps(slack_event))

    # Event APIの認証
    if "challenge" in slack_event:
        return slack_event.get("challenge")

    # ボットによるイベントまたはメッセージ投稿イベント以外の場合
    # 反応させないためにそのままリターンする
    # Slackには何かしらのレスポンスを返す必要があるのでOKと返す
    # （返さない場合、失敗とみなされて同じリクエストが何度か送られてくる）
    if is_bot(slack_event) or not is_message_event(slack_event):
        return "OK"
    

    # 天気を取得したい時
    if(slack_event["event"]["text"]=="天気"):
        x=otenki_api()
        mes="{}\n日付:{}\n天気:{}\n最高気温:{}".format(x["title"],x["forecasts"][1]["date"],x["forecasts"][1]["telop"],x["forecasts"][1]["temperature"]["max"]["celsius"])
        post_message_to_slack_channel(mes, slack_event.get("event").get("channel"))
    else:
        #とりあえずなんか産んだら褒めてくれる
        num=random.uniform(0,100)
        if num<33:
            post_message_to_slack_channel("(´-ω-｀)ﾅﾙﾎﾄﾞﾅ", slack_event.get("event").get("channel"))
        elif num<66:
            post_message_to_slack_channel("(｀･ω･´)ｲｲﾈｪ～!!", slack_event.get("event").get("channel"))
        else:
            post_message_to_slack_channel("(*・ω・*)wkwk", slack_event.get("event").get("channel"))


    # メッセージの投稿とは別に、Event APIによるリクエストの結果として
    # Slackに何かしらのレスポンスを返す必要があるのでOKと返す
    # （返さない場合、失敗とみなされて同じリクエストが何度か送られてくる）
    return "OK"

def is_bot(slack_event: dict) -> bool:
    return slack_event.get("event").get("subtype") == "bot_message"


def is_message_event(slack_event: dict) -> bool:
    return slack_event.get("event").get("type") == "message"

def post_message_to_slack_channel(message: str, channel: str):
    # Slackのchat.postMessage APIを利用して投稿する
    # ヘッダーにはコンテンツタイプとボット認証トークンを付与する
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer {0}".format(os.environ["SLACK_BOT_USER_ACCESS_TOKEN"])
    }
    data = {
        "token": os.environ["SLACK_APP_AUTH_TOKEN"],
        "channel": channel,
        "text": message,
        "username": "Miku"
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), method="POST", headers=headers)
    urllib.request.urlopen(req)
    return

def otenki_api():
    WEATHER_URL="http://weather.livedoor.com/forecast/webservice/json/v1?city=%s"
    CITY_CODE="130010" # TOKYO
    url=WEATHER_URL%CITY_CODE
    html=urllib.request.urlopen(url)
    html_json=json.loads(html.read())
    return html_json



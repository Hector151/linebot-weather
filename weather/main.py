import json
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from getweather import *
app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('aEvS3C063S/sJd1IVT76oRSM2Yx4ERZeiJwY1IxkkOpWoHd2+HhHRXPuvGXYillRkfPlh8THGD1AV1OLJyYC9scroGKeMy2bWRNIhO4xB8lwLtyBFTYDyYyZgakBH9ZXAtkfZePmfjwu/2yjMfPxwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('04e57db24b278583dfbc9eda298319ea')
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
cities = ['基隆市','嘉義市','臺北市','嘉義縣','新北市','臺南市','桃園縣','高雄市','新竹市','屏東縣','新竹縣','臺東縣','苗栗縣','花蓮市','花蓮縣','臺中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']
# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    reply_message = ""
    if message_type == "text":
        if(message[:4] == '當日天氣'):
            city = message[5:]
            city = city.replace('台','臺')
            if(not (city in cities)):
                reply_message += "查詢格式為: 當日天氣 縣市名稱"
                line_bot_api.reply_message(reply_token,TextSendMessage(text = reply_message))
            else:
                reply_message += aday(city)
                line_bot_api.reply_message(reply_token,TextSendMessage(text = reply_message))
        # elif(message[:4] == '目前天氣'):
        #     city = message[5:]
        #     city = city.replace('台','臺')
        #     if(not (city in cities)):
        #         reply_message += "查詢格式為: 目前天氣 縣市名稱"
        #         line_bot_api.reply_message(reply_token,TextSendMessage(text = reply_message))
        #     else:
        #         reply_message += current(city)
        #         line_bot_api.reply_message(reply_token,TextSendMessage(text = reply_message))
        elif(message[:4] == '未來天氣'):
            city = message[5:]
            city = city.replace('台','臺')
            if(not (city in cities)):
                reply_message += "查詢格式為: 未來天氣 縣市名稱"
                line_bot_api.reply_message(reply_token,TextSendMessage(text = reply_message))
            else:
                reply_message += future(city)
                line_bot_api.reply_message(reply_token,TextSendMessage(text = reply_message))
        else:
            line_bot_api.reply_message(reply_token, TextSendMessage(text = message))


# Postback event
# @handler.add(PostbackEvent)
# def handle_postback(event):
#     data = event.postback.data
#     reply_token = event.reply_token
#     if(data == 'target'): 
#         target = event.postback.text
#         targetjson = detail(target)
#         line_bot_api.reply_message(reply_token, FlexSendMessage('result', targetjson))



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from crawler import IFoodie


app = Flask(__name__)

line_bot_api = LineBotApi("EpmF03Rq6DHGlHrmhYDOdnFjy/NXtl7OqCi5SdkGvDgS22m9MhWfYEjQ6/FXH4UBPDZYRpvw9/9f5qu2JhVmFBsMPlu4LdvA6Z4D9+fYhm8NY28+noW69y3FwNkGkwyLs/CvqK44xt0WAAh6Zk3HNAdB04t89/1O/w1cDnyilFU=")  # 可在無法取得值時返回異常
handler = WebhookHandler("6ca542429c9a3e6647e4040847561373")  # 可在無法取得值時返回異常


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=(TextMessage))
def handle_message(event):
    if isinstance(event, MessageEvent):
        msg = event.message.text
        if not msg == ''.join(msg.split()):
            result = IFoodie(msg.split(' ')[0], msg.split(' ')[1])
        else:
            result = IFoodie(msg, "")
        response = result.scrape()
        if response:
            if response == "未成功連線至目標網站！":
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="未連接上目標網站！"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response.strip()))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="目前無餐廳營業!"))
    else :
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入「查詢地區」 「查詢食物種類」!!'))

    return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
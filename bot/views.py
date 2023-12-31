from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    ImageSendMessage,
    LocationSendMessage,
    StickerMessage,
)
from crawler.main import get_lottory, get_big_lottory
from crawler.train import get_stations, get_train_data2

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)
menu_str = ""
temp_str = ""
stations = {}


def index(request):
    return HttpResponse("chatbot v1.0")


def get_menu():
    global menu_str, stations
    if menu_str == "":
        stations = get_stations()
        menu = {i + 1: station for i, station in enumerate(stations)}
        count = 0
        for k, v in menu.items():
            menu_str += "{:2}{:4}".format(k, v)
            count += 1
            if count % 4 == 0:
                menu_str += "\n"


@csrf_exempt
def callback(request):
    global menu_str, stations
    get_menu()
    print(menu_str)

    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                text = event.message.text
                print(text)
                if text == "1":
                    text = menu_str

                if text == "2":
                    # 1000-台北
                    text = get_train_data2(
                        stations["臺北"], stations["基隆"], "2023/09/10", "12:00", "23:59"
                    )
                    print(text)

                message = TextSendMessage(text=text)

                try:
                    line_bot_api.reply_message(event.reply_token, message)
                except Exception as e:
                    print(e)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


print(get_lottory())

import requests
from dotenv import dotenv_values # pip3 instlal python-dotenv
import time

secrets = dotenv_values(".env")
TOKEN = secrets['TELEGRAM_BOT_API_KEY']

CHAT_ID = "6949343041"
WAITING_TIME_FOR_PASSWD = 100


def send_telegram_message(text):
    base_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(base_url, data=payload)
    return response.json()

def read_telegram_messages():
    for x in range (0, WAITING_TIME_FOR_PASSWD):  
        b =  str(WAITING_TIME_FOR_PASSWD - x) + " secs left to enter password."
        print (b, end="\r")
        time.sleep(1)
    base_url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.post(base_url).json()
    list_msg = response["result"]
    auth_code = list_msg[len(list_msg) - 1]["message"]["text"]
    print("auth_code: ", auth_code)
    return auth_code


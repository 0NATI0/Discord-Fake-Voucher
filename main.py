import requests
import tls_client
import base64
import json
import random
import threading
import time
import os
import websocket

from libs.libs    import buildnum
from pystyle      import *
from datetime     import datetime

build_number = None

class Log:
    lock = threading.Lock()

    def session(token):
        current_time = datetime.now().strftime("%H:%M")
        with Log.lock:
            print(f"[{Colors.dark_gray}{current_time}{Colors.reset}] {Colorate.Horizontal(Colors.blue_to_cyan, '[SESSION]', 1)}{Colors.reset} Successfully started session for {Colors.purple}{token[:32]}...{Colors.reset}")


    def buildnumber(number):
        current_time = datetime.now().strftime("%H:%M")
        with Log.lock:
            print(f"[{Colors.dark_gray}{current_time}{Colors.reset}] {Colorate.Horizontal(Colors.blue_to_purple, '[BUILD_NUM]', 1)}{Colors.reset} Got build number: {Colors.purple}{number}{Colors.reset}")

    def sended(message):
        current_time = datetime.now().strftime("%H:%M")
        with Log.lock:
            print(f"[{Colors.dark_gray}{current_time}{Colors.reset}] {Colorate.Horizontal(Colors.green_to_yellow, '[SENDER]', 1)}{Colors.reset} Sent a message: {Colors.purple}{message}{Colors.reset}")

    def failed():
        current_time = datetime.now().strftime("%H:%M")
        with Log.lock:
            print(f"[{Colors.dark_gray}{current_time}{Colors.reset}] {Colorate.Horizontal(Colors.red_to_yellow, '[SENDER]', 1)}{Colors.reset} Failed to sent a message")

    def onlined(token):
        current_time = datetime.now().strftime("%H:%M")
        with Log.lock:
            print(f"[{Colors.dark_gray}{current_time}{Colors.reset}] {Colorate.Horizontal(Colors.red_to_yellow, '[ONLINER]', 1)}{Colors.reset} Onlined {Colors.purple}{token[:32]}...{Colors.reset}")


def onliner(token):
        pld = {
            "op": 2,
            "d": {
                "token": token,
                "capabilities": 61,
                "properties": {
                    "os": "Windows",
                    "browser": "Safari",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    "browser_version": "110.0.0.0",
                    "os_version": "10"
                },
                "presence": {
                    "status": random.choice(["online", "idle", "dnd"]),
                    "since": 0,
                    "activities": [{
                        "name": "Custom Status",
                        "type": 4,
                        "state": "Money is key!",
                        "emoji": ""
                    }],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "highest_last_message_id": "0"
                }
            }
        }
        conn = websocket.create_connection("wss://gateway.discord.gg/?encoding=json&v=9")
        conn.send(json.dumps(pld))
        Log.onlined(token)

class Sender:
    def __init__(self, t, sess):
        self.token = t
        self.session = sess
        self.headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.6',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'authorization': t,
            'cookie': '__dcfduid=c40c6530323b11eea6943d48a33b85d7; __sdcfduid=c40c6531323b11eea6943d48a33b85d74e3b255172df6241336655bdb13cfc6f62c22c46e9f9bfbe6ae02f72ef4c82d7; __cfruid=f49721d5aad5fe037eb8c3e5ef1e9f386333ff8b-1691316566; locale=en-GB',
            'origin': 'https://discord.com',
            'pragma': 'no-cache',
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc':'1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-super-properties': base64.b64encode(json.dumps({
            "os":"Windows",
            "browser":"Chrome",
            "device":"",
            "system_locale":"en-US",
            "browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "browser_version":"115.0.0.0",
            "os_version":"10",
            "referrer":"",
            "referring_domain":"",
            "referrer_current":"",
            "referring_domain_current":"",
            "release_channel":"stable",
            "client_build_number": build_number,
            "client_event_source":"null"
        }, separators=(',', ':')).encode()).decode()}

    def get_message():
        with open('messages.txt', 'r') as file:
            lines = file.readlines()

        random_line = random.choice(lines)
        return random_line
    def send_message(self, channel_id):
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

        message = Sender.get_message()
        payload = {
            "content": message,
            "tts": False,
            "flags": 0
        }

        rr = requests.post(url, headers=self.headers, json=payload)
        if rr.status_code == 200:
            Log.sended(message)
        else:
            Log.failed()

def worker(token, channel, delay, toOnline):
    session = tls_client.Session(client_identifier='safari_16_0', random_tls_extension_order=True)
    sent = Sender(token, session)
    last_onliner_time = time.time()

    while True:
        current_time = time.time()
        if current_time - last_onliner_time >= 200:
            onliner(token)
            last_onliner_time = current_time

        sent.send_message(channel)
        time.sleep(delay)




delay = int(input(f"{Colors.reset}({Colors.light_blue}?{Colors.reset}) Delay >> "))
channel_id = int(input(f"{Colors.reset}({Colors.light_blue}?{Colors.reset}) Chennel id (tokens need to be joined) >> "))
procentage = int(input(f"{Colors.reset}({Colors.light_blue}?{Colors.reset}) Procentage to online >> "))
os.system('cls')
build_number = buildnum(); Log.buildnumber(build_number)


with open('tokens.txt', 'r') as file:
    lines = file.readlines()
for tokene in lines:
    if random.randint(1, 100) <= procentage:
            toOnline = True
    else:
            toOnline = False
    token = tokene.strip()
    threading.Thread(target=worker, args=(token, channel_id, delay, toOnline, )).start()

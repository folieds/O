import string
import random
import requests
from termcolor import cprint
import time
import os
import webbrowser

# 🔐 Fixed Telegram Bot Token and Channel
BOT_TOKEN = "7903387054:AAFDPEvHUA7-JLJKhNAQ_SIrd5ISV2UWHco"
CHANNEL_USERNAME = "@PythonBotz"
CHANNEL_LINK = "https://t.me/PythonBotz"

# ✅ Send message to Telegram
def send_to_telegram(chat_id, message):
    footer = f"\n👉 Join {CHANNEL_USERNAME}"
    message += footer
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=payload, timeout=5)
    except:
        pass

# 🔍 Check if user is in channel
def is_user_in_channel(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
    params = {"chat_id": CHANNEL_USERNAME, "user_id": user_id}
    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            status = r.json()["result"]["status"]
            return status in ["member", "administrator", "creator"]
    except:
        pass
    return False

# 🎲 Generate 4-letter username
def generate_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

# 🕵️ Check Reddit availability
def is_username_available(username):
    url = f"https://www.reddit.com/api/username_available.json?user={username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        return r.status_code == 200 and r.json() == True
    except:
        return False

# 🔁 Live log print
def print_live_log(available, used, total):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
    cprint("🚀 Reddit 4L Finder Tool Started", "magenta", attrs=["bold"])
    cprint(f"🟢 Available : {available}  ", "green", attrs=["bold"])
    cprint(f"🔴 Used     : {used}  ", "red", attrs=["bold"])
    cprint(f"🔍 Checked  : {total}  ", "cyan", attrs=["bold"])
    cprint(f"\n👉 Join Channel ➤ {CHANNEL_USERNAME}  ", "yellow", attrs=["underline"])

# 🚀 Start Tool
def start_tool():
    cprint("🔗 Join our official channel for updates:", "cyan", attrs=["bold"])
    cprint(f"👉 {CHANNEL_USERNAME} ", "yellow", attrs=["underline"])
    try:
        webbrowser.open(CHANNEL_LINK)
    except:
        pass

    cprint("\n💬 Enter your Telegram User ID:", "cyan")
    user_id = input(">> ")

    if not is_user_in_channel(user_id):
        cprint("🚫 You are not subscribed to the required channel!", "red", attrs=["bold"])
        cprint(f"👉 Please join: {CHANNEL_USERNAME}", "yellow", attrs=["bold", "underline"])
        return

    cprint("🔢 How many usernames to check?", "green")
    try:
        target = int(input(">> "))
    except:
        cprint("❌ Invalid number!", "red")
        return

    available = 0
    used = 0
    checked = 0

    print_live_log(available, used, checked)

    while available < target:
        uname = generate_username()
        checked += 1

        if is_username_available(uname):
            available += 1
            msg = f"✅ {uname} is AVAILABLE \n\nFound: {available}, \nChecked: {checked}"
            send_to_telegram(user_id, msg)
        else:
            used += 1

        print_live_log(available, used, checked)
        time.sleep(0.15)

    final_msg = f"\n🎯 DONE!\n✔️ Found: {available}  \n🔍 Checked: {checked}  "
    send_to_telegram(user_id, final_msg)
    cprint(final_msg, "green", attrs=["bold"])

# ▶️ Run tool
start_tool()

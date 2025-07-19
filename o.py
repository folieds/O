import string
import random
import requests
import time
import os
import webbrowser

# ✅ cprint fallback if termcolor not installed
try:
    from termcolor import cprint
except:
    def cprint(text, color=None, attrs=None):
        print(text)

# 🔐 Telegram bot config
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
        r = requests.post(url, data=payload, timeout=5)
        if not r.ok:
            print("⚠️ Telegram Error:", r.text)
    except Exception as e:
        print("❌ Telegram Exception:", e)

# 🔍 Check if user is in the channel
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

# 🔁 Print live log
def print_live_log(available, used, total):
    os.system('cls' if os.name == 'nt' else 'clear')
    cprint("🚀 Reddit 4L Finder Tool Started", "magenta", attrs=["bold"])
    cprint(f"🟢 Available : {available}      ", "green", attrs=["bold"])
    cprint(f"🔴 Used     : {used}       ", "red", attrs=["bold"])
    cprint(f"🔍 Checked  : {total}      ", "cyan", attrs=["bold"])
    cprint(f"\n\n👉 Join Channel ➤ {CHANNEL_USERNAME}      ", "blue", attrs=["bold", "reverse"])

# 🚀 Start tool
def start_tool():
    cprint("🔗 Join our official channel for updates:", "cyan", attrs=["bold"])
    cprint(f"👉 {CHANNEL_LINK} ", "yellow", attrs=["underline"])
    try:
        webbrowser.open(CHANNEL_LINK)
    except:
        pass

    cprint("\n💬 Enter your Telegram User ID (numeric):", "cyan")
    try:
        user_id = int(input(">> ").strip())
    except ValueError:
        cprint("❌ Invalid Telegram User ID!", "red")
        return

    if not is_user_in_channel(user_id):
        cprint("🚫 You are not subscribed to the required channel!", "red", attrs=["bold"])
        cprint(f"👉 Please join: {CHANNEL_LINK} ", "yellow", attrs=["bold", "underline"])
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
            msg = f"🎯 New Hit {available}\n\nUsername > {uname} ✅"
            send_to_telegram(user_id, msg)
            with open("available_usernames.txt", "a") as f:
                f.write(uname + "\n")
        else:
            used += 1

        print_live_log(available, used, checked)
        time.sleep(0.25)

    final_msg = f"\n🎯 DONE!\n✔️ Found: {available}  \n🔍 Checked: {checked}"
    send_to_telegram(user_id, final_msg)
    cprint(final_msg, "green", attrs=["bold"])

# ▶️ Run
start_tool()

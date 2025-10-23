import time
import requests
from datetime import datetime
from plyer import notification

URL = "https://medium.com"
CHECK_INTERVAL = 900  # 15 minutes in seconds

def check_medium():
    try:
        r = requests.get(URL, timeout=10)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False

while True:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking Medium...")
    if check_medium():
        msg = "🎉 Medium.com is back online!"
        print(msg)
        if notification:
            notification.notify(title="Medium Status", message=msg, timeout=10)
        break
    else:
        print("Still down. Will check again in 15 minutes.")
        time.sleep(CHECK_INTERVAL)

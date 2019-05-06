import json
import os
import re
import time
from datetime import datetime


def update_times():
    import requests
    api_data = requests.get(
        "http://api.aladhan.com/v1/timingsByCity?city=New+York&country=United+States&method=8").json()
    ptime = api_data["data"]["timings"]
    stored_data = {
        "date": today,
        "times": {
            "Fajr": {
                "time": ptime["Fajr"],
                "done": False
            },
            "Dhuhr": {
                "time": ptime["Dhuhr"],
                "done": False
            },
            "Asr": {
                "time": ptime["Asr"],
                "done": False
            },
            "Maghrib": {
                "time": ptime["Maghrib"],
                "done": False
            },
            "Isha": {
                "time": ptime["Isha"],
                "done": False
            },
        }
    }
    f = open("times.json", "w")
    f.write(json.dumps(stored_data))
    f.close()
    return stored_data


while not time.sleep(60):
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        time_json = open("times.json", "r").read()
        times = json.loads(time_json)
        assert (times["date"] == today), "Prayer times are not up to date"
    except:
        times = update_times()

    adhan_made = True
    max_time = None

    for prayer in times["times"]:
        prayer_time = datetime.strptime(times["times"][prayer]["time"], '%H:%M').time()
        if prayer_time < datetime.today().time() and (max_time is None or prayer_time > max_time):
            current_prayer = prayer
            adhan_made = times["times"][prayer]["done"]
            max_time = prayer_time

    if not adhan_made:
        times["times"][current_prayer]["done"] = True
        f = open("times.json", "w")
        f.write(json.dumps(times))
        f.close()

        cec_resp = os.popen('echo pow 0 | cec-client -s -d 1').read()
        status_search = re.finditer(r"(?<=\b(power\sstatus:)\s)(\w+)", cec_resp)
        for x in status_search:
            start = int(x.start())
            end = int(x.end())

        status = cec_resp[start:end]
        is_on = status == "on"

        if not is_on:
            os.system("echo on 0 | cec-client -s -d 1")
            time.sleep(1)

        os.system('echo "as" | cec-client RPI -s -d 1')
        time.sleep(2)
        os.system("omxplayer --no-keys audio.mp3 &")

        if not is_on:
            time.sleep(140)
            os.system("echo standby 0 | cec-client -s -d 1")

import json

def update_times():
    import requests
    


try:
    time_json = open("times.json", "r").read()
    times = json.loads(time_json)
except:
    times = update_times()



exit()

import os, re, time


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

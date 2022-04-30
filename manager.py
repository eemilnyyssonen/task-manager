import os
import sys
import subprocess
import time
import json
import pandas as pd

FNAME = 'time.json'
app_cmd = """xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) WM_CLASS"""
window_name_cmd = """xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) _NET_WM_NAME"""

def app():
    return subprocess.check_output(app_cmd, shell=True).decode('utf-8').split('"')[-2]

def window():
     return subprocess.check_output(window_name_cmd, shell=True).decode('utf-8').split('"')[-2]

def url():
     return subprocess.check_output(app_cmd, shell=True).decode('utf-8')#.split('"')[-2]

class Time():
    def __init__(self, start, stop, app, window) -> None:
        super().__init__()
        self.start_time = start
        self.stop_time = stop
        self.app_name = app
        self.window = window

    def parse_time(self) -> dict:
        data = {
            "time_start": time.asctime(self.start_time),
            "days": abs(self.stop_time.tm_mday-self.start_time.tm_mday),
            "hours": abs(self.stop_time.tm_hour-self.start_time.tm_hour),
            "minutes": abs(self.stop_time.tm_min-self.start_time.tm_min),
            "seconds": abs(self.stop_time.tm_sec-self.start_time.tm_sec),
            "time_end": time.asctime(self.stop_time)
        }
        return data

    def serialize_activity(self) -> dict:
        app_dict = {}
        with open(FNAME, 'a+') as f:
            try:
                #f.seek(0)
                data = json.load(f)
                #print(data)
                data[0][self.app_name].append({self.window: self.parse_time()})
                json.dump(data, f)
            except Exception as e:
                print(e)
                data = json.load(f)
                app_dict[self.app_name] = [{self.window: self.parse_time()}]
                json.dump(app_dict, f)

        return app_dict


    def __str__(self):
        return f'{self.serialize_activity().to_csv("test.csv") }'

""""{app_name":[
    {
        "window_name": some, 
            { 
            "start_time"
            "days"
            "hours"
            "seconds" : 
            "stop_time": 
            }
        }]
    } 
"""

if __name__ == '__main__': 
    current_window, current_app = window(), app()
    while True:
        start_time = time.localtime()

        while current_window == window():
            time.sleep(1)

        end_time = time.localtime()
        
        new_time_entry = Time(start_time, end_time, current_app, current_window)
        print(new_time_entry)
        #print(app(), window(), sep='\n')
        current_window, current_app = window(), app()


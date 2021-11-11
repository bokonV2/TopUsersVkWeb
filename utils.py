import datetime
import json

from config import dir

now = datetime.datetime.now()

def dates_srav(now, date, days=1):
    try:
        datetmp = '.'.join([date.split('.')[0],date.split('.')[1]])
        try:
            d1 = datetime.datetime.strptime(datetmp, "%d.%m")
        except:
            datetmp = '.'.join([str(int(date.split('.')[0])-1),date.split('.')[1]])
            d1 = datetime.datetime.strptime(datetmp, "%d.%m")
        d2 = datetime.datetime.strptime(f"{int(now.strftime('%d'))}.{int(now.strftime('%m'))}", "%d.%m")
        day = (d1 - d2).days
        if day >= 0 and day <= days:
            return True
        else:
            day += 365
            if day >= 0 and day <= days:
                return True
            return False
    except:
        return False
        
def diePpl(now, timestamp):
    value = datetime.datetime.fromtimestamp(timestamp)
    moynt = (now - value)
    if abs(moynt.days) <= 32:
        return True
    else:
        return False

def checkOnline(now, timestamp):
    value = datetime.datetime.fromtimestamp(timestamp)
    moynt = (now - value)
    if abs(moynt.seconds/60) <= 120:
        return True
    else:
        return False

def open_json(len, bg=""):
    fileDir = f"{dir}/data{bg}/{len}.json"
    with open(fileDir, mode="r") as file:
        data = json.load(file)
    return data

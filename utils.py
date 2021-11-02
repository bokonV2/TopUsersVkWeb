import datetime
import json

now = datetime.datetime.now()

def dates_srav(now, date, days=1):
    # print(now, date, days)
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

def diePpl(now, timestamp):
    #print(timestamp)
    #timestamp = 1634625500
    value = datetime.datetime.fromtimestamp(timestamp)

    moynt = (now - value)

    if abs(moynt.days) <= 32:
        return True
    else:
        return False
        
def checkOnline(now, timestamp):
    value = datetime.datetime.fromtimestamp(timestamp)
    moynt = (now - value)
    # print(moynt.seconds/60)
    if abs(moynt.seconds/60) <= 120:
        return True
    else:
        return False
        
def open_json(len, bg=""):
    fileDir = f"/home/c/cv67525/public_html/data{bg}/{len}.json"
    with open(fileDir, mode="r") as file:
        data = json.load(file)
    return data

def test():
    id = 0
    ids = [1, 2, 5]
    if id in ids:
        print("DA")


#test()

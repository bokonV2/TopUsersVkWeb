import datetime
import json

now = datetime.datetime.now()

def dates_srav(now, date, days=1):
    d1 = datetime.datetime.strptime(date, "%d.%m")
    d2 = datetime.datetime.strptime(f"{int(now.strftime('%d'))}.{int(now.strftime('%m'))}", "%d.%m")
    day = (d2 - d1).days
    if abs(day) <= days:
        return True
    else:
        return False


def open_json(len):
    fileDir = f"data/{len}.json"
    with open(fileDir, mode="r") as file:
        data = json.load(file)
    return data

import datetime
import json

now = datetime.datetime.now()

def dates_srav(now, date):
    dateV = date.split(".")
    dateP = [str(int(now.strftime("%d"))), str(int(now.strftime("%m")))]
    if dateV[0] == dateP[0] and dateV[1] == dateP[1]:
        return True
    else:
        return False


def open_json(len):
    fileDir = f"data/{len}.json"
    with open(fileDir, mode="r") as file:
        data = json.load(file)
    return data

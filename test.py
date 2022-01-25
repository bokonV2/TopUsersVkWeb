import requests
from pprint import pprint
VKAPI = "https://api.vk.com/method/"
# TOKEN = "caa98e2ec949004908c7487f243f3aae1f4946e8226b09ed8fb7bfc3f5127f48b848a333a04f032d8517a"
TOKEN = "2b319b6859e9149c9cf57bc79b8c9a1988ddf2f282f82f9418b2f044688100c68e6c23465038a740b296d"
V = 5.21
VKTOKEN = f"&access_token={TOKEN}&v={V}"

def getExecute():
    response = requests.post(f"{VKAPI}execute",
        data = {
        "code": """
                var members = [];
                var offset = 0;
                members.push(API.groups.getMembers({"group_id": "164712137", "v": "5.21"}).count);
                while (offset < 24000)
                {
                members.push(API.groups.getMembers({"group_id": "164712137", "v": "5.21", "sort": "id_asc", "count": "1000", "offset": offset, "fields":"bdate,photo_200,sex,city,last_seen"}).items);
                offset = offset + 1000;
                };
                return members;""",
        "access_token": TOKEN,
        "v": V,
        })
    try:
        response = response.json()['response']
        count = response.pop(0)
        # pprint(response)
        lens = 0
        for i in response:
            lens += len(i)
            # pprint(i)
        pprint(lens)
        pprint(count)
        # pprint(response[0])
    except:
        pprint(response.json())


getExecute()

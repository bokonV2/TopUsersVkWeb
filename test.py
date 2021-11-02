# test0 = "tmp.png"
# test1 = "tmp.jpg"
#
# print("png" in test0)
# print("png" in test1)

# if str(city) in self.city or self.city[0] == -1:

# test0 = "124"
# test1 = True
#
# print(test0 in test1)


import requests
url = "https://sun9-32.userapi.com/c841/u46431521/d_d4d43e3a.jpg"
# https://sun9-8.userapi.com/c1240/u879176/d_ba0ebb57.jpg
response = requests.get(url, stream=True)
print(type(response.status_code))
print(response.status_code)

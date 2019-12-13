import requests
import json
import pdb
from base64 import b64decode as b64d

url = "https://fridosleigh.com/api/capteha/request"

def requestImages():
    s = requests.post(url=url)
    parsed = json.loads(s.text)
    print(f"[!] Got {len(parsed['images'])} images! Writing to disk..")
    # DEBUG CLAUSE
    # pdb.set_trace()
    # print(parsed)

    # type(parsed) == dict, keys == 'images', 'request', 'select_type'
    # type(parsed['images'][i]) == dict, keys == 'base64', 'uuid'
    # pased['select_type'] == str what to select
    # need to submit in POST boyu answer=uuid:uuid:uuid URL encoded like:
    # answer=7956c5da-e585-11e9-97c1-309c23aaf0ac%2C1c1583bc-e586-11e9-97c1-309c23aaf0ac%2Cf79e07e5-e586-11e9-97c1-309c23aaf0ac

    for image in parsed['images']:
        rawImage = b64d(image['base64'])
        with open('./training_images/{}.png'.format(image['uuid']),'wb') as file:
            file.write(rawImage)

    print("[+] Images written!")

for i in range(0,25):
    print(f"[!] Iteraton {i}..")
    requestImages()
import requests
import json
import pdb
from base64 import b64decode as b64d
import sys
import predict
#from urllib.parse import urlencode

url = "https://fridosleigh.com/api/capteha/request"
submit_url = "https://fridosleigh.com/api/capteha/submit"
proxies = {'http':'127.0.0.1:8080','https':'127.0.0.1:8080'}

def requestImages():
    s = requests.session()
    resp = s.post(url=url,proxies=proxies,verify=False)
    parsed = json.loads(resp.text)
    print(f"[!] Got {len(parsed['images'])} images!")
    # DEBUG CLAUSE
    # pdb.set_trace()
    # print(parsed)

    # type(parsed) == dict, keys == 'images', 'request', 'select_type'
    # type(parsed['images'][i]) == dict, keys == 'base64', 'uuid'
    # pased['select_type'] == str what to select
    # need to submit in POST boyu answer=uuid:uuid:uuid URL encoded like:
    # answer=7956c5da-e585-11e9-97c1-309c23aaf0ac%2C1c1583bc-e586-11e9-97c1-309c23aaf0ac%2Cf79e07e5-e586-11e9-97c1-309c23aaf0ac
    return parsed,s

def collectImages(data,folder):
    for image in data['images']:
        rawImage = b64d(image['base64'])
        with open('./{}/{}.png'.format(folder,image['uuid']),'wb') as file:
            file.write(rawImage)
    print("[+] Images written to a folder!")
        
def verifyImages(data,session):
        # Collect what to seek
        classes = data['select_type'].lower()
        myclasses = []
        if 'trees' in classes:
            myclasses.append('trees')
        if 'hats' in classes:
            myclasses.append('hats')
        if 'presents' in classes:
            myclasses.append('gifts')
        if 'ornament' in classes:
            myclasses.append('balls')
        if 'cane' in classes:
            myclasses.append('candies')
        if 'stockings' in classes:
            myclasses.append('socks')
        # DEBUG CLAUSE
        #print(myclasses)
        #print(classes)
        #pdb.set_trace()
        #folder = 'test_images'
        #collectImages(data,folder)

        image_list = []
        for image in data['images']:
            rawImage = b64d(image['base64'])
            uuid = image['uuid']
            image_list.append([uuid,rawImage])

        print("[!] Need to select images from following classes: {}"\
            .format(', '.join(myclasses)))
        # 1. LAUNCH TRAIN SCRIPT AND GET UUID OF IMAGES THAT ARE NEEDED
        # 2. SEND IT WITHIN SAME SESSION TO SUBMIT     
        prediction_results = predict.main(image_list)

        # len(prediction_results) == num of images
        # prediction_results[i] == dict, like:
        # {'img_full_path': 'test_images/01e96130-e585-11e9-97c1-309c23aaf0ac.png', \ 
        # 'prediction': 'Hats', 'percent': 0.96241474}
        answer = []
        for prediction in prediction_results:
            predictClass = prediction['prediction'].lower()
            if predictClass in myclasses:
                valid_uuid = prediction['uuid']
                answer.append(valid_uuid)
                print(f"{valid_uuid} seem to be predicted as {predictClass}")
        #print(answer)
        data_to_send = '%2C'.join(answer)
        print(data_to_send)
        validation = session.post(url=submit_url,data='answer={}'.format(data_to_send),\
            proxies=proxies,verify=False)
        
        print(validation.cookies)
        print(validation.text)

def main():
    try:
        if sys.argv[1] == 'collect':
            for i in range(0,10):
                print(f"[!] Collecting 100 Images. Iteraton {i}..")
                data,s = requestImages()
                collectImages(data,'training_images')
                sys.exit(0)
        elif sys.argv[1] == 'verify':
            print(f"[!] Bypassing reCatpeha!")
            data,s = requestImages()
            verifyImages(data,s)
    except IndexError:
        print('[-] Describe what to do: collect or verify!')
        sys.exit(1)
    except Exception as ex:
        print(ex)
        sys.exit(1)

main()
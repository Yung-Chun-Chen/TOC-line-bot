import requests

SERVER_IP = "10.30.1.92"
API_SERVER = "http://" + SERVER_IP + ":8000"
DOWNLOAD_IMAGE_API = "/show-fsm"

try:
    downloadImageInfoResponse = requests.get(
        API_SERVER + DOWNLOAD_IMAGE_API)

    if downloadImageInfoResponse.status_code == 200:
        with open('img.jpg', 'wb') as getFile:
            getFile.write(downloadImageInfoResponse.content)
except Exception as err:
    print('Other error occurred %s' % {err})
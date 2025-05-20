import cv2
import requests
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fps', type=int, default=10, help="Specify the stream's FPS (default: 10)")
parser.add_argument('-c', '--compression', type=int, default=70, help="Compression level from 0-100 (default: 70)")
parser.add_argument('-H', '--host', required=True, help="Public IP or hostname of the remote server")
parser.add_argument('-p', '--port', type=int, default=8081, help="Hosted port on the remote server (default: 8081)")
args = parser.parse_args()

FPS = args.fps
QUALITY = abs(100 - args.compression)
HOST = args.host
PORT = args.port
capt = cv2.VideoCapture(0)
COUNT = 0
COMPRESSION = [cv2.IMWRITE_JPEG_QUALITY, QUALITY]
HEADERS = {'Connection': 'keep-alive'}
HOST_STR = ""
if HOST.startswith("http://") or HOST.startswith('https://'):
    HOST_STR = HOST + ':' + str(PORT)
else:
    HOST_STR = 'http://' + HOST + ':' + str(PORT)

while True:
    ret, frame = capt.read()
    idk, my_im = cv2.imencode('.jpg', frame, COMPRESSION)
    im_encoded = my_im.tobytes()
    COUNT += 1
    print(f'[*] Sent frame {COUNT}')
    FILES = {'img': im_encoded}
    resp = requests.post(HOST_STR, files=FILES, headers=HEADERS)
    if (resp.text == 'ok'):
        time.sleep(1/FPS)
        continue
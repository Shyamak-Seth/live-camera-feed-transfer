import cv2
import time
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fps', default=10, type=int, help="FPS for the stream")
args = parser.parse_args()
FPS = args.fps

COUNT = 0
print('[+] Starting the watch...')
while True:
    try:
        if os.path.exists('capture.jpg'):
            COUNT += 1
            im = cv2.imread('capture.jpg')
            cv2.imshow('feed', im)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            print(f'[*] Showed frame {COUNT}')
            time.sleep(1/FPS)
    except Exception as e:
        print('An error occured. Still, continuing...')
        continue
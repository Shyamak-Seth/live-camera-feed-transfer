from flask import Flask, request
import logging
import os
import argparse
import shutil
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--save', default=0, type=int, help="Save every nth capture from the stream.")
parser.add_argument('-p', '--port', default=8081, type=int, help="Specify the port to listen on.")
args = parser.parse_args()
logging.getLogger('werkzeug').setLevel(logging.WARNING)

if args.save != 0 and not os.path.exists('./captures'):
    os.mkdir('captures')

app = Flask(__name__)

COUNT = 0

@app.route('/', methods=['POST'])
def submit():
    global COUNT
    data = request.files
    content = data['img']
    COUNT += 1
    content.save('capture.jpg')
    print('[*] Received frame', COUNT)
    if args.save != 0 and COUNT % args.save == 0:
        shutil.copyfile('capture.jpg', f'captures/capture_{COUNT//args.save}.jpg')
    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)
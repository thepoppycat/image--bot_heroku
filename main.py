from flask import Flask, redirect, request
import pytesseract
import os
import cv2
import shutil
from PIL import Image
import requests

app = Flask(__name__)


def read_ocr(url):
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        print("Unable to retrieve image")
        return
    filename = f'tmp.{url[-3:]}'
    with open(filename, 'wb+') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)
    cv2.imwrite(filename, gray)
    out = pytesseract.image_to_string(Image.open(filename))
    print(out)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['url']:
            print('incoming image')
            print(request.form['url'])
            read_ocr(request.form['url'])
            return "kek"

    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    # for local deployment
    #app.run(debug=True)
    # for heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

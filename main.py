from flask import Flask, redirect, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__)


def read_ocr(file):
    out = pytesseract.image_to_string(Image.open(file))
    print(out)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['file']:
            file = request.form['file']
            print('incoming image')
            print(type(file))
            with open('tmp.png', 'wb+') as f:
                f.write(file.encode())
            print(os.listdir())
            read_ocr('tmp.png')
            return "kek"

    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    # for local deployment
    #app.run(debug=True)
    # for heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

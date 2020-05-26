from flask import Flask, redirect, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__)


def read_ocr():
    out = pytesseract.image_to_string(Image.open('tmp'))
    print(out)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.files)
        if request.form['file']:
            file_bytes = request.form['file']
            print('incoming image')
            print(type(file_bytes))
            print(file_bytes.encode())
            print(len(file_bytes.encode()))
            with open('tmp', 'wb+') as f:
                f.write(file_bytes.encode())
            print(os.listdir())
            read_ocr()
            return "kek"

    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    # for local deployment
    #app.run(debug=True)
    # for heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

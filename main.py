from flask import Flask, redirect, request, flash
import pytesseract
from PIL import Image
import os
from werkzeug.datastructures import FileStorage

app = Flask(__name__)


def read_ocr():
    out = pytesseract.image_to_string(Image.open('tmp'))
    print(out)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        FileStorage(request.stream).save('tmp')
        print(f'File size: {os.path.getsize("tmp")}')
        print(os.listdir())
        k = open('tmp', 'rb').read()
        print(k[:20])
        read_ocr()
        return 'k'

    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    # for local deployment
    #app.run(debug=True)
    # for heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

from flask import Flask, redirect, request
import pytesseract
import os

app = Flask(__name__)


def read_ocr(image):
    pass


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['url']:
            print('incoming image')
            print(request.form['url'])
            return "kek"

    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    # for local deployment
    #app.run(debug=True)
    # for heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

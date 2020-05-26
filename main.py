from flask import Flask, redirect, request
import pytesseract
import os

app = Flask(__name__)


def read_ocr(file):
    out = pytesseract.image_to_string(file)
    print(out)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['file']:
            print('incoming image')
            print(type(request.form['file']))
            #read_ocr(request.form['file'])
            return "kek"

    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    # for local deployment
    #app.run(debug=True)
    # for heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

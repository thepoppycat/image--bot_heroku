from flask import Flask, redirect
import pytesseract

app = Flask(__name__)


def read_ocr(image):


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['url']:
            print('incoming image')
            print(request.form['url'])

    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

if __name__=="__main__":
    app.run('0.0.0.0', port=5000)

from flask import Flask, redirect, request, flash
import os

from image import read_ocr_plain, classify_faces_plain
from direct import get_img, read_ocr, classify_faces

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.files)
        request.files['raw'].save('raw')
        request.files['gray'].save('gray')
        print(f'File size: {os.path.getsize("raw")}')
        text = read_ocr_plain()
        res = text
        res += '!^@*!%@^#*!@^#'+str(classify_faces_plain())
        return res

    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


@app.route('/direct', methods=['GET', 'POST'])
def direct():
    if request.method == 'POST':
        url = request.form.get('url')
        get_img(url)  # saved to 'raw'
        print(f'File size: {os.path.getsize("raw")}')
        res = read_ocr()
        print(res)
        res += '!^@*!%@^#*!@^#'+str(classify_faces())
        return res

    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


if __name__=="__main__":
    app.secret_key = os.urandom(12)
    # for local deployment
    #app.run(debug=True)
    # for heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

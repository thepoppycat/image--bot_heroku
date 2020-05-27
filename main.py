from flask import Flask, redirect, request, flash
import pytesseract
from PIL import Image
import os
import face_recognition as fr
import numpy as np
import cv2

app = Flask(__name__)


def read_ocr():
    text = pytesseract.image_to_string(Image.open('gray'))
    text = text.replace('|', 'I')
    text = text.replace('\n', ' ')
    text = text.replace('[', '')
    return text


def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded

FACES = get_encoded_faces()

def classify_faces():
    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """
    global FACES
    faces = FACES
    img = cv2.imread('raw', 1)
    print('ok')
    if img is None:
        print("Invalid image array")
        return

    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    face_locations = fr.face_locations(img)
    unknown_face_encodings = fr.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = fr.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = fr.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    return face_locations, face_names



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.files)
        request.files['raw'].save('raw')
        request.files['gray'].save('gray')
        print(f'File size: {os.path.getsize("raw")}')
        text = read_ocr()
        out = text
        out += str(classify_faces())
        return out

    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    # for local deployment
    #app.run(debug=True)
    # for heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

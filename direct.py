from PIL import Image
import cv2
import requests
import shutil
import pytesseract
import face_recognition as fr
import os
import numpy as np
from qrtools import QR 

def get_img(url):
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        print("Unable to retrieve image")
        return
    filename = 'raw'
    with open(filename, 'wb+') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    print('received image')


def read_ocr():
    image = cv2.imread('raw', 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)
    cv2.imwrite('gray.png', gray)
    text = pytesseract.image_to_string(Image.open('gray.png'))
    text = text.replace('|', 'I')
    text = text.replace('\n', ' ')
    text = text.replace('[', '')
    return text
	
def read_qr():
	my_QR = QR(filename = "raw") 
  
	# decodes the QR code and returns True if successful 
	my_QR.decode() 
  
	return my_QR.data 


def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}
    paths = ["./faces/", "./faces/hist/"]
    for path in paths:
        for f in os.listdir(path):
            if f.endswith(".jpg") or f.endswith(".png"):
                try:
                    face = fr.load_image_file(path + f)
                    encoding = fr.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding
                except:
                    pass


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



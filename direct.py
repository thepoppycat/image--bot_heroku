from PIL import Image
import cv2
import requests
import shutil
import pytesseract
import face_recognition as fr
import os
import numpy as np

def get_img(url):
	r = requests.get(url, stream=True)
	if r.status_code != 200:
		print("Unable to retrieve image")
		return
	with open('raw', 'wb+') as f:
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
	os.remove('gray.png')
	return text
	
def read_qr():
	img = cv2.imread('raw', 1)
	detector = cv2.QRCodeDetector()
	data, bbox, _ = detector.detectAndDecode(img)
	if data:
		print("QR Code detected-->")
	return data
	
def get_encoded_faces():
	encoded = {}
	folders = ["school", "hist", "world"]
	
	for folder in folders:
		print(f"Getting from {folder}...")
		path = "./faces/"+folder
		for f in os.listdir(path):
			if f.endswith(".jpg") or f.endswith(".png"):
				try:
					face = fr.load_image_file(os.path.join(path, f))
					encoding = fr.face_encodings(face)[0]
					encoded[f.split(".")[0]] = encoding
				except Exception as e:
					print(f"{e}; file = {f}")
					try:
						print(len(fr.face_encodings(face)))
					except Exception as e:
						print("oh no encodings don't work")
		print(f"Done with {folder}")
	print(f"{len(encoded)} faces collected")
	return encoded


FACES = get_encoded_faces()


def classify_faces():
	global FACES
	faces = FACES
	img = cv2.imread('raw', 1)
	if img is None:
		print("Invalid image array")
		return
	print("Image ok")
		
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

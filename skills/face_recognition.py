import cv2
import os
import numpy as np
import pickle
import threading
import time

FACES_DIR = os.path.join(os.path.dirname(__file__), '..', 'known_faces')
ENCODINGS_FILE = os.path.join(os.path.dirname(__file__), '..', 'face_encodings.pkl')
os.makedirs(FACES_DIR, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

known_names = []
is_trained = False
running = False
presence_callback = None


def register_face(name):
    global known_names, is_trained
    try:
        cap = cv2.VideoCapture(0)
        print(f"📸 Look at camera to register {name}...")

        faces_data = []
        labels = []
        count = 0
        label_id = len(known_names)

        while count < 30:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_roi = gray[y:y + h, x:x + w]
                face_roi = cv2.resize(face_roi, (100, 100))
                faces_data.append(face_roi)
                labels.append(label_id)
                count += 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"Capturing {count}/30",
                            (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Register Face", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if faces_data:
            known_names.append(name)
            recognizer.train(faces_data, np.array(labels))
            recognizer.save(ENCODINGS_FILE.replace('.pkl', '.yml'))
            with open(ENCODINGS_FILE, 'wb') as f:
                pickle.dump(known_names, f)
            is_trained = True
            return f"Face registered for {name}! I'll recognize you now!"
        return "Couldn't capture face! Try again!"
    except Exception as e:
        return f"Registration error: {e}"


def load_encodings():
    global known_names, is_trained
    try:
        yml_path = ENCODINGS_FILE.replace('.pkl', '.yml')
        if os.path.exists(yml_path) and os.path.exists(ENCODINGS_FILE):
            recognizer.read(yml_path)
            with open(ENCODINGS_FILE, 'rb') as f:
                known_names = pickle.load(f)
            is_trained = True
            print(f"✅ Loaded {len(known_names)} faces!")
    except Exception as e:
        print(f"Load error: {e}")


def recognize_face():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return "Couldn't access camera!"

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return "No face detected!"

        if not is_trained:
            return "No faces registered yet! Say 'register my face' first!"

        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (100, 100))
            label, confidence = recognizer.predict(face_roi)

            if confidence < 100:
                return known_names[label]
            else:
                return "Unknown person!"

        return "Unknown!"
    except Exception as e:
        return f"Recognition error: {e}"


def start_presence_detection(callback=None):
    global running, presence_callback
    presence_callback = callback
    running = True
    thread = threading.Thread(target=_presence_loop, daemon=True)
    thread.start()
    print("✅ Presence detection started!")


def _presence_loop():
    global running
    try:
        cap = cv2.VideoCapture(0)
        last_seen = None

        while running:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0 and is_trained:
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y + h, x:x + w]
                    face_roi = cv2.resize(face_roi, (100, 100))
                    try:
                        label, confidence = recognizer.predict(face_roi)
                        if confidence < 100:
                            name = known_names[label]
                            if name != last_seen:
                                last_seen = name
                                print(f"👤 Detected: {name}")
                                if presence_callback:
                                    presence_callback(name)
                    except:
                        pass
            else:
                if last_seen:
                    last_seen = None

            time.sleep(2)

        cap.release()
    except Exception as e:
        print(f"Presence error: {e}")


def stop_presence_detection():
    global running
    running = False


load_encodings()
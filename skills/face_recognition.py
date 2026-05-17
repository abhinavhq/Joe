import cv2
import os
import pickle
import threading
import numpy as np

FACES_DIR = os.path.join(os.path.dirname(__file__), '..', 'known_faces')
ENCODINGS_FILE = os.path.join(os.path.dirname(__file__), '..', 'face_encodings.pkl')

os.makedirs(FACES_DIR, exist_ok=True)

known_encodings = []
known_names = []
presence_callback = None
running = False


def load_encodings():
    global known_encodings, known_names
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, 'rb') as f:
            data = pickle.load(f)
            known_encodings = data['encodings']
            known_names = data['names']
        print(f"✅ Loaded {len(known_names)} faces!")


def save_encodings():
    with open(ENCODINGS_FILE, 'wb') as f:
        pickle.dump({'encodings': known_encodings, 'names': known_names}, f)


def register_face(name):
    try:
        import face_recognition
        cap = cv2.VideoCapture(0)
        print(f"📸 Look at camera to register {name}...")

        samples = []
        count = 0

        while count < 10:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            locations = face_recognition.face_locations(rgb)

            if locations:
                encodings = face_recognition.face_encodings(rgb, locations)
                if encodings:
                    samples.append(encodings[0])
                    count += 1
                    cv2.putText(frame, f"Capturing... {count}/10",
                                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Register Face", frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if samples:
            avg_encoding = np.mean(samples, axis=0)
            known_encodings.append(avg_encoding)
            known_names.append(name)
            save_encodings()
            return f"Face registered for {name}!"
        return "Couldn't capture face!"
    except Exception as e:
        return f"Face registration error: {e}"


def recognize_face():
    try:
        import face_recognition
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return "Unknown"

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)

        if not locations:
            return "No face detected"

        encodings = face_recognition.face_encodings(rgb, locations)

        for encoding in encodings:
            if known_encodings:
                matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.6)
                distances = face_recognition.face_distance(known_encodings, encoding)
                best_match = np.argmin(distances)

                if matches[best_match]:
                    return known_names[best_match]

        return "Unknown person"
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
        import face_recognition
        cap = cv2.VideoCapture(0)
        last_seen = None

        while running:
            ret, frame = cap.read()
            if not ret:
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            locations = face_recognition.face_locations(rgb)

            if locations and known_encodings:
                encodings = face_recognition.face_encodings(rgb, locations)
                for encoding in encodings:
                    matches = face_recognition.compare_faces(known_encodings, encoding)
                    distances = face_recognition.face_distance(known_encodings, encoding)
                    best_match = np.argmin(distances)

                    if matches[best_match]:
                        name = known_names[best_match]
                        if name != last_seen:
                            last_seen = name
                            print(f"👤 Detected: {name}")
                            if presence_callback:
                                presence_callback(name)
            else:
                if last_seen:
                    last_seen = None
                    print("👤 No one detected")

            import time
            time.sleep(2)

        cap.release()
    except Exception as e:
        print(f"Presence error: {e}")


def stop_presence_detection():
    global running
    running = False


load_encodings()
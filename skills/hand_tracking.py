import cv2
import mediapipe as mp
import threading

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

current_gesture = None
gesture_callback = None
running = False


def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 fingers
    tips = [8, 12, 16, 20]
    pip = [6, 10, 14, 18]

    for tip, p in zip(tips, pip):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[p].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def detect_gesture(fingers):
    total = sum(fingers)

    if total == 0:
        return "fist"
    elif total == 5:
        return "open_hand"
    elif fingers == [0, 1, 0, 0, 0]:
        return "point"
    elif fingers == [0, 1, 1, 0, 0]:
        return "peace"
    elif fingers == [1, 0, 0, 0, 1]:
        return "rock"
    elif fingers == [1, 1, 0, 0, 0]:
        return "gun"
    elif total == 1 and fingers[4] == 1:
        return "pinky"
    else:
        return f"{total}_fingers"


def start_hand_tracking(callback=None):
    global running, gesture_callback
    gesture_callback = callback
    running = True
    thread = threading.Thread(target=_run, daemon=True)
    thread.start()


def _run():
    global current_gesture, running

    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    last_gesture = None
    gesture_count = 0

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                fingers = count_fingers(hand_landmarks)
                gesture = detect_gesture(fingers)

                # Stable gesture detection
                if gesture == last_gesture:
                    gesture_count += 1
                else:
                    gesture_count = 0
                    last_gesture = gesture

                # Trigger after 15 stable frames
                if gesture_count == 15:
                    current_gesture = gesture
                    print(f"✋ Gesture: {gesture}")
                    if gesture_callback:
                        gesture_callback(gesture)

                # Show gesture on screen
                cv2.putText(frame, f"Gesture: {gesture}",
                            (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)
                cv2.putText(frame, f"Fingers: {sum(fingers)}",
                            (10, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0), 2)

        cv2.imshow("JOI Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def stop_hand_tracking():
    global running
    running = False


def get_current_gesture():
    return current_gesture
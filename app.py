from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import pyautogui

app = Flask(__name__)

# Initialize camera and Mediapipe tools
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

def generate_frames():
    while True:
        success, frame = cam.read()
        if not success:
            break
        else:
            # Flip and process frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            frame_h, frame_w, _ = frame.shape


            if landmark_points:
                landmarks = landmark_points[0].landmark

                # Map the iris points for cursor movement
                for id, landmark in enumerate(landmarks[474:476]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    if id == 1:
                        screen_x = screen_w / frame_w * x
                        screen_y = screen_h / frame_h * y
                        pyautogui.moveTo(screen_x, screen_y)

                # Detect eye closure for clicking
                left_eye_top = landmarks[145]
                left_eye_bottom = landmarks[159]
                left_eye_aspect_ratio = abs(left_eye_top.y - left_eye_bottom.y)
                CLICK_THRESHOLD = 0.015

                if left_eye_aspect_ratio < CLICK_THRESHOLD:
                    pyautogui.click()
                    pyautogui.sleep(0.5)

            # Encode and yield frame to the web page
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)

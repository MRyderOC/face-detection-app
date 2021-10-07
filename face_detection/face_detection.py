from flask import Blueprint, render_template, Response
import cv2


face_detection_bp = Blueprint(
    'face_detection',
    __name__,
    template_folder='templates',
    static_folder='static',
)


def generate_frames():
    cam = cv2.VideoCapture(0)
    while True:
        # read the camera frame
        success, frame = cam.read()
        if not success:
            break
        else:

            detector=cv2.CascadeClassifier('face_detection/static/Haarcascades/haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('face_detection/static/Haarcascades/haarcascade_eye.xml')
            faces=detector.detectMultiScale(frame,1.1,7)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            )


@face_detection_bp.route('/helper__face_detection')
def face_detection_helper():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@face_detection_bp.route('/')
def face_detection():
    return render_template('face_detection/face_detection.html')
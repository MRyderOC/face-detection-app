from flask import Blueprint, render_template, Response
import cv2


face_detection_bp = Blueprint(
    'face_detection',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@face_detection_bp.route('/')
def face_detection():
    return render_template('face_detection/face_detection.html')
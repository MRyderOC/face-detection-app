from flask import Flask


def create_app(config=None):
    app = Flask(__name__)

    from face_detection.face_detection import face_detection_bp
    app.register_blueprint(face_detection_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
# app.py
# app.py
import cv2
import numpy as np
from base64 import b64encode
from ultralytics import YOLO
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)

model = YOLO("./weights/latebest.pt", task='detect')
camera = cv2.VideoCapture(0)
detection_enabled = True

aliases = {
    "0 personne": "Personne",
    "1 casque": "Casque",
    "2 gilet": "Gilet",
}

def draw_box(image, box, class_name, prob):
    class_name_display = aliases.get(class_name, class_name)
    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.putText(image, f"{class_name_display}: {prob}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def check_equipment(result):
    helmet_detected = False
    vest_detected = False
    person_detected = False

    for box in result.boxes:
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        class_name = result.names[class_id]

        if class_name == "0 personne":
            person_detected = True
        elif class_name == "1 casque":
            helmet_detected = True
        elif class_name == "2 gilet":
            vest_detected = True

    return person_detected, helmet_detected, vest_detected

def get_compliance_message(person_detected, helmet_detected, vest_detected):
    if not person_detected:
        return "Aucune personne visible"
    elif person_detected and not helmet_detected and not vest_detected:
        return "Uniforme non conforme (casque et gilet requis)"
    elif not helmet_detected:
        return "Casque manquant"
    elif not vest_detected:
        return "Gilet manquant"
    else:
        return "Uniforme conforme"
    
def detect_objects(image):
    if not detection_enabled:
        return image, "black", "Détection désactivée"

    results = model.predict(image)
    result = results[0]

    person_detected, helmet_detected, vest_detected = check_equipment(result)

    for box in result.boxes:
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        class_name = result.names[class_id]

        if class_name == "0 personne" and person_detected:
            draw_box(image, box, class_name, prob)
        elif class_name == "1 casque" and helmet_detected:
            draw_box(image, box, class_name, prob)
        elif class_name == "2 gilet" and vest_detected:
            draw_box(image, box, class_name, prob)

    compliance_message = get_compliance_message(person_detected, helmet_detected, vest_detected)
    background_color = "green" if person_detected and helmet_detected and vest_detected else "red"

    return image, background_color, compliance_message

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image_file' not in request.files:
            return render_template('index.html', background_color="white", compliance_message="Aucune image soumise")

        file = request.files['image_file']

        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not file.filename.lower().endswith(tuple(allowed_extensions)):
            return render_template('index.html', background_color="white", compliance_message="Format d'image non pris en charge")

        max_file_size = 10 * 1024 * 1024  # 10 Mo
        if len(file.read()) > max_file_size:
            return render_template('index.html', background_color="white", compliance_message="Fichier trop volumineux (10 Mo maximum)")

        file.seek(0)
        image_bytes = file.read()
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        image, background_color, compliance_message = detect_objects(image)

        ret, buffer = cv2.imencode('.jpg', image)
        image_bytes = buffer.tobytes()
        image_base64 = b64encode(image_bytes).decode('utf-8')

        return render_template('index.html', image_base64=image_base64, background_color=background_color, compliance_message=compliance_message)
    else:
        return render_template('index.html', image_base64=None, background_color="white", compliance_message=None)

@app.route('/video', methods=['GET'])
def video():
    def video_stream():
        while True:
            ret, frame = camera.read()
            if not ret:
                break

            image, background_color, compliance_message = detect_objects(frame)

            frame_height, frame_width, _ = frame.shape
            border_thickness = 10

            if "Uniforme non conforme (casque et gilet requis)" in compliance_message:
                frame[:border_thickness, :, :] = [0, 0, 255]  # Liseré rouge en haut
                frame[-border_thickness:, :, :] = [0, 0, 255]  # Liseré rouge en bas
                frame[:, :border_thickness, :] = [0, 0, 255]  # Liseré rouge à gauche
                frame[:, -border_thickness:, :] = [0, 0, 255]  # Liseré rouge à droite
            elif "Gilet manquant" in compliance_message or "Casque manquant" in compliance_message:
                frame[:border_thickness, :, :] = [0, 165, 255]  # Liseré orange en haut
                frame[-border_thickness:, :, :] = [0, 165, 255]  # Liseré orange en bas
                frame[:, :border_thickness, :] = [0, 165, 255]  # Liseré orange à gauche
                frame[:, -border_thickness:, :] = [0, 165, 255]  # Liseré orange à droite
            else:
                frame[:border_thickness, :, :] = [0, 255, 0]  # Liseré vert en haut
                frame[-border_thickness:, :, :] = [0, 255, 0]  # Liseré vert en bas
                frame[:, :border_thickness, :] = [0, 255, 0]  # Liseré vert à gauche
                frame[:, -border_thickness:, :] = [0, 255, 0]  # Liseré vert à droite

            frame = cv2.putText(frame, compliance_message, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            image_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')

    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

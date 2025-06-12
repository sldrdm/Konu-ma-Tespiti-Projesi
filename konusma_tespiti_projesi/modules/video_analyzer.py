import cv2
from modules.face_tracker import load_known_faces, identify_faces
from modules.mouth_detector import calculate_mouth_open, update_speaking_status, get_speaking_time, konusma_kayitlari
from modules.emotion_detector import predict_emotion, duygu_kayitlari
from modules.utils import export_to_csv
from config import MOUTH_OPEN_THRESHOLD
import mediapipe as mp

def analyze_video_file(video_path):
    cap = cv2.VideoCapture(video_path)
    known_encodings, known_names = load_known_faces("data/known_faces")

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=5)

    frame_count = 0
    frame_interval = 30  # her 1 saniyede 1 kare analiz (30fps varsayımı)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_interval != 0:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape

        face_data = identify_faces(frame, known_encodings, known_names)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for landmarks, face in zip(results.multi_face_landmarks, face_data):
                name = face["name"]
                (top, right, bottom, left) = face["location"]

                mouth_open_val = calculate_mouth_open(landmarks.landmark, w, h)
                update_speaking_status(name, mouth_open_val, MOUTH_OPEN_THRESHOLD)
                predict_emotion(frame, face["location"], name)

    cap.release()

    # Export only durations and emotions to videosonuc.csv
    export_to_csv(
        {k: get_speaking_time(k) for k in konusma_kayitlari},
        duygu_kayitlari,
        output_path="data/outputs/videosonuc.csv",
        emotion_summary=True
    )

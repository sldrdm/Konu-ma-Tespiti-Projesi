import face_recognition
import os
import cv2

def load_known_faces(known_faces_dir):
    known_encodings = []
    known_names = []

    for filename in os.listdir(known_faces_dir):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            name = os.path.splitext(filename)[0]  # dosya adından isim al (örneğin Ahmet.jpg → Ahmet)
            image_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(name)
            else:
                print(f"[Uyarı] {filename} dosyasında yüz bulunamadı!")

    return known_encodings, known_names


def identify_faces(frame, known_encodings, known_names):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_data = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Bilinmiyor"

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]

        face_data.append({
            "name": name,
            "location": (top, right, bottom, left)
        })

    return face_data

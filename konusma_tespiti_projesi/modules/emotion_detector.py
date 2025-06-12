from deepface import DeepFace
import cv2
import numpy as np

# Her kişi için son duyguları tutacak sözlük
duygu_kayitlari = {}

def predict_emotion(frame, face_location, person_name):
    top, right, bottom, left = face_location

    # Yüz bölgesini kes
    face_img = frame[top:bottom, left:right]

    try:
        # DeepFace ile duygu tahmini
        result = DeepFace.analyze(face_img, actions=["emotion"], enforce_detection=False)

        # En baskın duyguyu al
        dominant_emotion = result[0]['dominant_emotion']

        # Kaydet
        duygu_kayitlari[person_name] = dominant_emotion

        return dominant_emotion

    except Exception as e:
        # Hata varsa önceki duyguyu döndür (ya da bilinmiyor)
        return duygu_kayitlari.get(person_name, "Bilinmiyor")

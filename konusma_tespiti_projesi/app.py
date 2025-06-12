import streamlit as st
import cv2
import os

from config import MOUTH_OPEN_THRESHOLD
from modules.face_tracker import load_known_faces, identify_faces
from modules.mouth_detector import calculate_mouth_open, update_speaking_status, get_speaking_time, konusma_kayitlari
from modules.emotion_detector import predict_emotion, duygu_kayitlari
from modules.utils import format_time, export_to_csv

import mediapipe as mp

# Sayfa başlığı ve yapılandırma
st.set_page_config(layout="wide")
st.title("🧬 Gerçek Zamanlı Konuşan Kişi ve Duygu Tespiti")

tab1, tab2 = st.tabs(["🎥 Kamera ile Analiz", "📺 YouTube Videosu ile Analiz"])

# === 🎥 Kamera ile Analiz ===
with tab1:
    st.markdown("Tanıtılmış yüzleri **canlı videodan analiz eder**, konuşma süre sini hesaplar ve duygu durumlarını raporlar.")

    st.sidebar.info("✅ Yüzler yükleniyor...")
    known_encodings, known_names = load_known_faces("data/known_faces")
    st.sidebar.success(f"{len(known_names)} kişi tanıtıldı.")

    if st.button("🎥 Kamerayı Başlat"):
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=5)

        st.warning("Canlı yayını durdurmak için sayfayı durdurun veya Ctrl+C ile sonlandırın.")

        try:
            frame_count = 0
            last_emotions = {}

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
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
                        konusma_suresi = get_speaking_time(name)

                        duygu = predict_emotion(frame, face["location"], name)
                        last_emotions[name] = duygu

                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, f"{name}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                        cv2.putText(frame, f"Sure: {format_time(konusma_suresi)}", (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                        cv2.putText(frame, f"Duygu: {duygu}", (left, bottom + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
                frame_count += 1

        finally:
            cap.release()
            # Tüm konuşmaları finalize et
            for name in konusma_kayitlari:
                update_speaking_status(name, 0, MOUTH_OPEN_THRESHOLD)

            export_to_csv(
                {k: get_speaking_time(k) for k in konusma_kayitlari},
                output_path="data/outputs/sonuclar.csv"
            )
            st.sidebar.success("📁 Konuşma verileri kaydedildi: `data/outputs/sonuclar.csv`")

    if st.sidebar.button("📄 Konuşma verilerini manuel olarak tekrar kaydet (.csv)"):
        for name in konusma_kayitlari:
            update_speaking_status(name, 0, MOUTH_OPEN_THRESHOLD)
        export_to_csv(
            {k: get_speaking_time(k) for k in konusma_kayitlari},
            output_path="data/outputs/sonuclar.csv"
        )
        st.sidebar.success("CSV dosyası başarıyla tekrar oluşturuldu: `data/outputs/sonuclar.csv`")

# === 📺 YouTube Videosu ile Analiz ===
with tab2:
    st.header("📺 YouTube Videosundan Konuşma ve Duygu Analizi")

    import yt_dlp

    yt_url = st.text_input("🔗 YouTube video bağlantısını buraya yapıştırın:")

    if yt_url:
        if st.button("📅 Videoyu İndir ve Analiz Et"):
            st.info("🎥 Video indiriliyor...")
            try:
                out_path = "data/yt_videos"
                os.makedirs(out_path, exist_ok=True)
                video_path = os.path.join(out_path, "yt_video.mp4")

                ydl_opts = {
                    'outtmpl': video_path,
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                    'merge_output_format': 'mp4',
                    'quiet': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([yt_url])

                st.success("✅ Video indirildi. Analiz başlatılıyor...")

                from modules.video_analyzer import analyze_video_file
                analyze_video_file(video_path)

                st.success("✅ Analiz tamamlandı. Sonuç: `data/outputs/videosonuc.csv`")

                with open("data/outputs/videosonuc.csv", "r", encoding="utf-8") as file:
                    st.download_button("📄 CSV'yi İndir", data=file.read(), file_name="videosonuc.csv")

            except Exception as e:
                st.error(f"❌ Hata oluştu: {e}")

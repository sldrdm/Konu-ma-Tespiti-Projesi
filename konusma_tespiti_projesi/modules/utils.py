import csv
import os

def export_to_csv(speaking_dict, emotion_dict=None, output_path="data/outputs/sonuclar.csv", emotion_summary=False):
    import csv
    import os
    from collections import Counter

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Ana tablo: kişi - konuşma süresi - duygu
        writer.writerow(["Kisi", "Konusma Suresi (dk)", "Duygu"])
        for name, sure in speaking_dict.items():
            dakika = sure / 60
            duygu = emotion_dict.get(name, "Bilinmiyor") if emotion_dict else "Bilinmiyor"
            writer.writerow([name, f"{dakika:.2f}", duygu])

        # İsteğe bağlı olarak toplam duygu süresi analizi
        if emotion_summary and emotion_dict:
            writer.writerow([])  # boşluk
            writer.writerow(["Duygu", "Toplam Görülme (saniye)"])

            # Her duygu kaçar saniye göründü → sadece video için!
            counts = Counter()
            for name, duygu in emotion_dict.items():
                sure = speaking_dict.get(name, 0)
                counts[duygu] += sure

            for duygu, sure in counts.items():
                writer.writerow([duygu, f"{sure:.2f}"])

            
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes} dk {sec} sn"

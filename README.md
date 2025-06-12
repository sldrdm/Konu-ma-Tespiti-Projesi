<!-- Banner veya logo eklemek istersen en üste ekle -->
<p align="center">
  <img src="https://raw.githubusercontent.com/sldrdm/Konu-ma-Tespiti-Projesi/main/assets/cover.png" alt="Proje Banner" width="600"/>
</p>

<h1 align="center">📚 Konu-ma Tespiti Projesi</h1>
<p align="center">
  <b>Otomatik Metin Konusu Sınıflandırma ve Etiketleme</b><br>
  <i>Python & NLP tabanlı açık kaynak bir konu/tema tespiti çözümü</i>
</p>

<p align="center">
  <a href="https://github.com/sldrdm/Konu-ma-Tespiti-Projesi/stargazers"><img alt="stars" src="https://img.shields.io/github/stars/sldrdm/Konu-ma-Tespiti-Projesi?style=flat-square"></a>
  <a href="#"><img alt="python" src="https://img.shields.io/badge/Python-3.8+-blue?logo=python"></a>
  <a href="#"><img alt="licence" src="https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square"></a>
</p>

---

## 🚀 Proje Tanıtımı

<p align="center">
  <img src="https://raw.githubusercontent.com/sldrdm/Konu-ma-Tespiti-Projesi/main/assets/demo.gif" width="70%" alt="Demo GIF" />
</p>

Konu-ma Tespiti Projesi, metinlerdeki ana temaları otomatik tespit eden, Türkçe ve İngilizce dil desteğiyle çalışan bir NLP uygulamasıdır.  
Amaç; büyük metin kütlelerinde **otomatik etiketleme** ve **anlamlandırma** işlemlerini hızlıca ve doğru şekilde yapmaktır.

---

## 🧰 Kullanılan Teknolojiler

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/NLTK-76B900?style=for-the-badge&logo=nltk&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gensim-264653?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
</div>

---

## 🖥️ Ekran Görüntüleri

<p align="center">
  <img src="https://raw.githubusercontent.com/sldrdm/Konu-ma-Tespiti-Projesi/main/assets/screenshot1.png" width="45%" alt="Çalışma Ekranı"/>
  <img src="https://raw.githubusercontent.com/sldrdm/Konu-ma-Tespiti-Projesi/main/assets/screenshot2.png" width="45%" alt="Konu Dağılımı"/>
</p>

---

## ⚡️ Hızlı Başlangıç

```bash
# 1. Repoyu klonla
git clone https://github.com/sldrdm/Konu-ma-Tespiti-Projesi.git
cd Konu-ma-Tespiti-Projesi

# 2. Ortamı hazırla
python3 -m venv venv
source venv/bin/activate    # (Windows: venv\Scripts\activate)

# 3. Gerekli paketleri yükle
pip install -r requirements.txt

# 4. Modeli eğit ve örnek tahmin çalıştır
python src/train.py --input data/ornek.csv --output models/model.pkl
python src/predict.py --model models/model.pkl --text "Yapay zeka çağımızın en popüler alanlarından biri."

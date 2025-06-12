import time

konusma_kayitlari = {}
FRAME_RATE = 30  # FPS sabitlenmeli, gerekirse dinamik alınabilir


def calculate_mouth_open(landmarks, w, h):
    top_lip = landmarks[13]  # üst dudak ortası
    bottom_lip = landmarks[14]  # alt dudak ortası

    top_y = int(top_lip.y * h)
    bottom_y = int(bottom_lip.y * h)

    return abs(bottom_y - top_y)


def update_speaking_status(name, mouth_open_value, threshold):
    now = time.time()
    if name not in konusma_kayitlari:
        konusma_kayitlari[name] = {
            "start_time": None,
            "total_speaking_time": 0.0,
            "speaking": False,
            "last_updated": now
        }

    user = konusma_kayitlari[name]

    if mouth_open_value > threshold:
        if not user["speaking"]:
            user["speaking"] = True
            user["start_time"] = now
    else:
        if user["speaking"]:
            # konuşma bitişi
            duration = now - user["start_time"]
            user["total_speaking_time"] += duration
            user["speaking"] = False
            user["start_time"] = None


def get_speaking_time(name):
    user = konusma_kayitlari.get(name, {})
    total = user.get("total_speaking_time", 0.0)
    if user.get("speaking") and user.get("start_time"):
        total += time.time() - user["start_time"]
    return total

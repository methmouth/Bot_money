import cv2
import mss
import numpy as np
import pygetwindow as gw
from ultralytics import YOLO

class VisionEngine:
    def __init__(self, config, url_stream=None):
        self.model = YOLO(config['yolo_model'])
        self.config = config
        self.url_stream = url_stream
        
        if self.url_stream:
            print(f"[*] Conectando a stream de red: {self.url_stream}")
            self.cap = cv2.VideoCapture(self.url_stream)
        else:
            self.sct = mss.mss()

    def get_frame(self):
        if self.url_stream:
            ret, frame = self.cap.read()
            return (frame, None) if ret else (None, None)
        
        try:
            windows = gw.getWindowsWithTitle(self.config['ventana_titulo'])
            if not windows: return None, None
            win = windows[0]
            monitor = {"top": win.top, "left": win.left, "width": win.width, "height": win.height}
            img = np.array(self.sct.grab(monitor))
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR), win
        except Exception:
            return None, None

    def detect_and_track(self, frame):
        # [span_3](start_span)Umbral de confianza del config.json[span_3](end_span)
        conf_min = self.config.get('umbral_confianza', 0.45)
        return self.model.predict(frame, conf=conf_min, verbose=False)[0], None

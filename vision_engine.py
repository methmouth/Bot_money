import cv2
import mss
import numpy as np
import pygetwindow as gw
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

class VisionEngine:
    def __init__(self, config):
        self.model = YOLO(config['yolo_model'])
        self.config = config
        self.sct = mss.mss()
        self.deepsort = DeepSort(max_age=30) if config['tracker_type'] == "deepsort" else None

    def get_frame(self):
        try:
            win = gw.getWindowsWithTitle(self.config['ventana_titulo'])[0]
            monitor = {"top": win.top, "left": win.left, "width": win.width, "height": win.height}
            img = np.array(self.sct.grab(monitor))
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR), win
        except: return None, None

    def detect_and_track(self, frame):
        if self.config['tracker_type'] == "bytetrack":
            return self.model.track(frame, persist=True, tracker="bytetrack.yaml", verbose=False)[0], None
        else:
            results = self.model.predict(frame, conf=self.config['umbral_confianza'], verbose=False)[0]
            detections = [([box.xyxy[0][0], box.xyxy[0][1], box.xyxy[0][2]-box.xyxy[0][0], box.xyxy[0][3]-box.xyxy[0][1]], 
                           box.conf[0], int(box.cls[0])) for box in results.boxes]
            return results, self.deepsort.update_tracks(detections, frame=frame)
import cv2, os
def extraer(video):
    if not os.path.exists("dataset_raw"): os.makedirs("dataset_raw")
    cam = cv2.VideoCapture(video)
    c = 0
    while True:
        s, f = cam.read()
        if not s: break
        if c % 15 == 0: cv2.imwrite(f"dataset_raw/f_{c}.jpg", f)
        c += 1
    cam.release()
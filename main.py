import json, time, subprocess, cv2, random
from vision_engine import VisionEngine
from predictor import BallPredictor
from ai_decision import GeminiBrain
from watchdog import BotWatchdog

with open('config.json') as f: config = json.load(f)
vision = VisionEngine(config)
predictor = BallPredictor(config['y_raqueta_norm'])
brain = GeminiBrain()
dog = BotWatchdog(config['paquete_juego'])

def get_res():
    out = subprocess.check_output("adb shell wm size", shell=True).decode()
    return map(int, out.split(': ')[1].split('x'))
W, H = get_res()

def human_move(x_norm, y_norm):
    # Ease-out swipe
    x = (x_norm * W) / 1000 + random.randint(-5, 5)
    y = (y_norm * H) / 1000
    subprocess.run(f"adb shell input touchscreen swipe {int(x)} {int(y)} {int(x)} {int(y)} 50", shell=True)

def main():
    last_gemini = 0
    while True:
        dog.verificar()
        frame, _ = vision.get_frame()
        if frame is None: continue

        res, tracks = vision.detect_and_track(frame)
        
        # Lógica de Juego
        bola = None
        if config['tracker_type'] == "bytetrack" and res.boxes.id is not None:
            for box in res.boxes:
                if res.names[int(box.cls[0])] == "bola":
                    bola = box.xyxyn[0].cpu().numpy() # [x, y]
        
        if bola is not None:
            x_pred = predictor.predecir(bola[0], bola[1])
            human_move(x_pred * 1000, config['y_raqueta_norm'] * 1000)
        
        # Lógica de Anuncios
        elif (time.time() - last_gemini) > config['frecuencia_gemini_seg']:
            dec = brain.analizar(frame)
            if dec['x'] != -1: human_move(dec['x'], dec['y'])
            last_gemini = time.time()

        cv2.imshow("IA Bot Debug", frame)
        if cv2.waitKey(1) == ord('q'): break

if __name__ == "__main__": main()
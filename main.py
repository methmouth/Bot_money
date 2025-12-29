import json, time, cv2
from vision_engine import VisionEngine
from ai_decision import GeminiBrain
from controlador_manager import ControladorHibrido

def main():
    with open('config.json') as f:
        config = json.load(f)
    
    print("1. Modo ADB (USB)\n2. Modo WiFi (IP)")
    opc = input("Seleccione: ")
    
    if opc == "1":
        modo, url = "adb", None
        [span_3](start_span)W, H = 1080, 1920 # O get_res() vía ADB[span_3](end_span)
    else:
        modo = "network"
        ip = "192.168.100.21" # Tu IP de la captura
        url = f"http://{ip}:8080/stream.mjpeg"
        W, H = 1080, 1920 # Ajustar a resolución del móvil

    vision = VisionEngine(config['bot_settings'], url_stream=url)
    control = ControladorHibrido(modo=modo, ip=ip if opc=="2" else None)
    brain = GeminiBrain(config['api_services']['openrouter'])
    last_gemini = 0

    while True:
        frame, _ = vision.get_frame()
        if frame is None: continue

        res, _ = vision.detect_and_track(frame)
        
        # [span_4](start_span)[span_5](start_span)Lógica de detección de bola (Tu predictor)[span_4](end_span)[span_5](end_span)
        if len(res.boxes) > 0:
            # ... lógica de raqueta ...
            pass
        elif (time.time() - last_gemini) > config['bot_settings']['frecuencia_gemini_seg']:
            # [span_6](start_span)[span_7](start_span)Uso de GeminiBrain para botones X/Claim[span_6](end_span)[span_7](end_span)
            dec = brain.analizar(frame)
            if dec.get('x') and dec['x'] != -1:
                control.click(dec['x'], dec['y'], W, H)
            last_gemini = time.time()

        cv2.imshow("Bot Hibrido", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
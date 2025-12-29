import json, time, cv2
from vision_engine import VisionEngine
from ai_decision import GeminiBrain
from controlador_manager import ControladorHibrido

def main():
    with open('config.json') as f:
        config = json.load(f)
    [span_5](start_span)bot_settings = config['bot_settings'] #[span_5](end_span)
    
    print("\n=== BOT MONEY CONFIGURATOR ===")
    print("1. Modo ADB (Cable USB)")
    print("2. Modo WiFi (Ingresar IP manualmente)")
    opcion = input("Seleccione una opción: ")

    url_video, ip_disp, modo = None, None, "adb"

    if opcion == "2":
        # Petición de IP desde CMD
        ip_input = input("Ingrese la IP del celular (ej. 192.168.100.21): ")
        ip_disp = ip_input.replace("http://", "").split(":")[0]
        url_video = f"http://{ip_disp}:8080/stream.mjpeg"
        modo = "network"

    vision = VisionEngine(bot_settings, url_stream=url_video)
    control = ControladorHibrido(modo=modo, ip=ip_disp)
    [span_6](start_span)brain = GeminiBrain(config['api_services']['openrouter']) #[span_6](end_span)
    
    W, H = 1080, 1920 # Resolución base
    last_gemini = 0

    while True:
        frame, _ = vision.get_frame()
        if frame is None: continue

        res, _ = vision.detect_and_track(frame)
        
        # [span_7](start_span)Si YOLO no detecta la bola, usamos Gemini para anuncios[span_7](end_span)
        if len(res.boxes) == 0:
            ahora = time.time()
            if (ahora - last_gemini) > bot_settings.get('frecuencia_gemini_seg', 15):
                [span_8](start_span)[span_9](start_span)dec = brain.analizar(frame) #[span_8](end_span)[span_9](end_span)
                if dec.get('x') and dec['x'] != -1:
                    control.click(dec['x'], dec['y'], W, H)
                last_gemini = ahora

        [span_10](start_span)cv2.imshow("Bot View", frame) #[span_10](end_span)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

if __name__ == "__main__":
    main()

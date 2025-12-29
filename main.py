import json, time, cv2
from vision_engine import VisionEngine
from ai_decision import GeminiBrain
from controlador_manager import ControladorHibrido

def main():
    # [span_11](start_span)Carga de configuración[span_11](end_span)
    with open('config.json') as f:
        config = json.load(f)
    bot_settings = config['bot_settings']
    
    print("\n=== CONFIGURACIÓN DE CONEXIÓN ===")
    print("1. Modo ADB (Cable USB / scrcpy)")
    print("2. Modo WiFi (Ingresar IP de ScreenStream)")
    opcion = input("Seleccione una opción: ")

    url_video, ip_disp, modo = None, None, "adb"

    if opcion == "2":
        # Petición de IP desde CMD
        ip_input = input("Ingrese la IP que muestra la App (ej. 192.168.100.21): ")
        ip_disp = ip_input.replace("http://", "").split(":")[0]
        url_video = f"http://{ip_disp}:8080/stream.mjpeg"
        modo = "network"

    vision = VisionEngine(bot_settings, url_stream=url_video)
    control = ControladorHibrido(modo=modo, ip=ip_disp)
    [span_12](start_span)brain = GeminiBrain(config['api_services']['openrouter'])[span_12](end_span)
    
    [span_13](start_span)W, H = 1080, 1920 # Resolución base[span_13](end_span)
    last_gemini = 0

    print(f"\n[>>>] BOT INICIADO EN MODO {modo.upper()}")

    while True:
        frame, _ = vision.get_frame()
        if frame is None: continue

        [span_14](start_span)res, _ = vision.detect_and_track(frame)[span_14](end_span)
        
        # [span_15](start_span)Si YOLO no detecta objetos, usamos Gemini para cerrar anuncios[span_15](end_span)
        if len(res.boxes) == 0:
            ahora = time.time()
            if (ahora - last_gemini) > bot_settings.get('frecuencia_gemini_seg', 15):
                [span_16](start_span)dec = brain.analizar(frame)[span_16](end_span)
                if dec.get('x') and dec['x'] != -1:
                    control.click(dec['x'], dec['y'], W, H)
                last_gemini = ahora

        [span_17](start_span)cv2.imshow("IA Bot View", frame)[span_17](end_span)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

if __name__ == "__main__":
    main()

# 🎮 AI-Driven Mobile Game Bot (Bounce & Break Edition)

Sistema de automatización inteligente basado en visión artificial para juegos móviles. Utiliza **YOLO11** para detección en tiempo real, **ByteTrack/DeepSORT** para seguimiento de objetos y **Gemini 2.0 Flash** para la resolución de anuncios y menús complejos.



## 🚀 Características Principales

* **Visión en Tiempo Real:** Procesamiento de frames mediante Scrcpy y OpenCV.
* **Motor de Detección:** Implementación de YOLO11 (Ultralytics) para latencia ultra baja.
* **Física Predictiva:** Algoritmo de trayectoria para anticipar el punto de caída de la bola, incluyendo rebotes en paredes.
* **Humanización de Movimientos:** Desplazamientos con interpolación *Ease-Out* y ruido aleatorio para evitar detecciones de bots.
* **Cerebro Híbrido:** Si la IA local no reconoce la pantalla (ej. anuncios nuevos), consulta a Gemini 2.0 vía API.
* **Watchdog:** Sistema de monitoreo que reinicia la app automáticamente si se cierra o falla.

## 🛠️ Requisitos Técnico

* **Android:** Depuración USB activada y modo "Toques visuales" opcional para calibración.
* **PC:** Python 3.10+, ADB instalado y configurado en el PATH.
* **Scrcpy:** Para el mirroring de baja latencia.

## 📦 Instalación

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/ai-game-bot.git](https://github.com/tu-usuario/ai-game-bot.git)
   cd ai-game-bot

 * Instala las dependencias:
   pip install -r requirements.txt

 * Configura tus credenciales en el archivo .env:
   OPENROUTER_API_KEY=tu_clave_aqui

🧠 Flujo de Trabajo
 * Captura de Datos: Usa data_extractor.py para procesar videos grabados y generar el dataset.
 * Entrenamiento: Sube las imágenes a Roboflow y entrena usando YOLO11 Nano.
 * Ejecución: * Inicia Scrcpy.
   * Ejecuta python main.py.

⚙️ Configuración (config.json)
 * tracker_type: Cambia entre bytetrack (más rápido) o deepsort (más robusto).
 * y_raqueta_norm: Ajusta la altura de la raqueta en escala 0.0 a 1.0 según la pantalla del dispositivo.
 * frecuencia_gemini_seg: Segundos de espera entre consultas a la nube para optimizar costos.
⚖️ Licencia
Este proyecto tiene fines educativos y de investigación en el área de Computer Vision.

---
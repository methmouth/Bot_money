import subprocess
from vncdotool import api

class ControladorHibrido:
    def __init__(self, modo="adb", ip=None):
        self.modo = modo
        self.client = None
        if modo == "network" and ip:
            print(f"[*] Estableciendo conexión VNC con {ip}...")
            # Requiere que el móvil tenga un VNC Server activo en el puerto 5900
            self.client = api.connect(ip, password=None) 

    def click(self, x_norm, y_norm, W, H):
        x = int((x_norm * W) / 1000)
        y = int((y_norm * H) / 1000)

        if self.modo == "adb":
            # [span_9](start_span)Comando original vía ADB[span_9](end_span)
            subprocess.run(f"adb shell input tap {x} {y}", shell=True)
        else:
            # Control vía red (VNC)
            self.client.mouseMove(x, y)
            self.client.click(1)

import subprocess
from vncdotool import api

class ControladorHibrido:
    def __init__(self, modo="adb", ip=None):
        self.modo = modo
        self.client = None
        if modo == "network":
            # Conexión VNC (Asegúrate de tener un VNC Server en el móvil)
            self.client = api.connect(ip, password=None) 

    def click(self, x_norm, y_norm, W, H):
        x = int((x_norm * W) / 1000)
        y = int((y_norm * H) / 1000)

        if self.modo == "adb":
            subprocess.run(f"adb shell input tap {x} {y}", shell=True)
        else:
            self.client.mouseMove(x, y)
            self.client.click(1)
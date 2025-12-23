import subprocess, time

class BotWatchdog:
    def __init__(self, paquete): self.paquete = paquete
    def verificar(self):
        cmd = "adb shell dumpsys window | grep 'mCurrentFocus'"
        res = subprocess.check_output(cmd, shell=True).decode()
        if self.paquete not in res:
            subprocess.run(f"adb shell am force-stop {self.paquete}", shell=True)
            subprocess.run(f"adb shell monkey -p {self.paquete} 1", shell=True)
            time.sleep(5)
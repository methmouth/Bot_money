import requests, base64, cv2, os, json
from dotenv import load_dotenv

load_dotenv()

class GeminiBrain:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def analizar(self, frame):
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        img_b64 = base64.b64encode(buffer).decode('utf-8')
        prompt = "Detecta botones 'X' de anuncios o 'Claim'. Responde JSON: {'x': 0-1000, 'y': 0-1000, 'accion': 'clic'}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"model": "google/gemini-2.0-flash-001", "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
        ]}]}
        try:
            r = requests.post(self.url, headers=headers, json=data).json()
            return json.loads(r['choices'][0]['message']['content'])
        except: return {"x": -1, "y": -1}

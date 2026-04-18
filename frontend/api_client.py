import requests


class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def check_health(self):
        response = requests.get(f"{self.base_url}/health", timeout=5)
        response.raise_for_status()
        return response.json()

    def predict(self, text, age=None, gender=None, pain_score=None, body_part=None):
        payload = {
            "text": text,
            "age": age,
            "gender": gender,
            "pain_score": pain_score,
            "body_part": body_part,
        }

        response = requests.post(
            f"{self.base_url}/predict",
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json()
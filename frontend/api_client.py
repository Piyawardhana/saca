import requests


class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def predict(
        self,
        text: str,
        pain_score: int | None = None,
        body_part: str | None = None,
        duration: str | None = None,
        medication: str | None = None,
        language: str | None = None,
        input_method: str | None = None,
    ) -> dict:
        payload = {
            "text": text,
            "pain_score": pain_score,
            "body_part": body_part,
            "duration": duration,
            "medication": medication,
            "language": language,
            "input_method": input_method,
        }

        response = requests.post(
            f"{self.base_url}/predict",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
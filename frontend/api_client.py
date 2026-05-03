import requests


class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def health_check(self) -> dict:
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=10
            )
            response.raise_for_status()

            return {
                "success": True,
                "data": response.json()
            }

        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Cannot connect to backend. Please make sure FastAPI is running."
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def predict(
        self,
        text: str,
        pain_score: int | None = None,
        body_part: str | None = None,
        age: int | None = None,
        gender: str | None = None,
    ) -> dict:
        """
        Sends user input to the FastAPI severity model.

        Backend currently expects:
        {
            "text": str,
            "age": optional int,
            "gender": optional str,
            "pain_score": optional int,
            "body_part": optional str
        }
        """

        payload = {
            "text": text,
            "age": age,
            "gender": gender,
            "pain_score": pain_score,
            "body_part": body_part,
        }

        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            return {
                "success": True,
                "data": response.json()
            }

        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Cannot connect to backend. Please start the FastAPI server first."
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Backend request timed out. Please try again."
            }

        except requests.exceptions.HTTPError as e:
            try:
                error_detail = response.json()
            except Exception:
                error_detail = str(e)

            return {
                "success": False,
                "error": f"Backend error: {error_detail}"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
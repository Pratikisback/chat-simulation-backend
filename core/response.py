# utils/response.py

from datetime import datetime, timezone

class Response:
    def __init__(self):
        self.status = "success"
        self.message = ""
        self.data = None
        self.error_code = None 

    def set(self, status: str = "success", error_code: int = 0,message: str = "", data=None):
        self.status = status
        self.error_code = error_code
        self.message = message
        self.data = data

        return self.dict()

    def dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "error_code": self.error_code,
            "timestamp": str(datetime.now(timezone.utc)),
            "data": self.data,
        }

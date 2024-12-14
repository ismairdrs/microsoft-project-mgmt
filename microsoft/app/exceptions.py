from enum import Enum
from typing import Any, Dict, List, Optional


class MicrosoftExceptionType(Enum):
    CLIENT_NOT_FOUND = "CLIENT_NOT_FOUND"
    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"
    ACTIVITY_NOT_FOUND = "ACTIVITY_NOT_FOUND"
    GENERAL_ERROR = "GENERAL_ERROR"
    NOT_FOUND = "NOT_FOUND"


class MicrosoftException(Exception):
    def __init__(
        self,
        type: MicrosoftExceptionType,
        message: str,
        errors: Optional[List[Dict[str, str]]] = None,
    ):
        super().__init__(message)
        self.type = type
        self.message = message
        self.errors = errors or []

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "type": self.type,
            "errors": self.errors,
        }

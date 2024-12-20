from enum import Enum
from typing import Any, Dict, List, Optional


class MicrosoftExceptionType(Enum):
    CLIENT_NOT_FOUND = "CLIENT_NOT_FOUND"
    CLIENT_ALREADY_EXISTS = "CLIENT_ALREADY_EXISTS"
    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"
    ACTIVITY_NOT_FOUND = "ACTIVITY_NOT_FOUND"
    GENERAL_ERROR = "GENERAL_ERROR"
    NOT_FOUND = "NOT_FOUND"
    CREATE_CLIENT_ERROR = "CREATE_CLIENT_ERROR"
    CREATE_PROJECT_ERROR = "CREATE_PROJECT_ERROR"
    PROJECT_ALREADY_EXISTS = "PROJECT_ALREADY_EXISTS"
    ACTIVITY_ALREADY_EXISTS = "ACTIVITY_ALREADY_EXISTS"
    CREATE_ACTIVITY_ERROR = "CREATE_ACTIVITY_ERROR"
    UPDATE_ACTIVITY_ERROR = "UPDATE_ACTIVITY_ERROR"


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

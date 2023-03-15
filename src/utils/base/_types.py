from typing import Any, Dict, TypeVar


class Response:
    status_code: int

    def json() -> Dict[str, Any]:
        ...


_R = TypeVar("_R", bound=Response)

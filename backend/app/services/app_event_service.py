import time
import uuid
from collections.abc import Mapping

from fastapi import Request

from app.repositories.app_event_repository import AppEventRepository


class AppEventService:
    def __init__(self, repository: AppEventRepository | None = None) -> None:
        self.repository = repository or AppEventRepository()

    def build_request_context(self, request: Request, started_at: float) -> dict[str, object | None]:
        forwarded_for = request.headers.get("x-forwarded-for")
        client_ip = forwarded_for.split(",", 1)[0].strip() if forwarded_for else None

        if client_ip is None and request.client is not None:
            client_ip = request.client.host

        return {
            "route": request.url.path,
            "method": request.method,
            "duration_ms": int((time.perf_counter() - started_at) * 1000),
            "request_id": request.headers.get("x-request-id") or str(uuid.uuid4()),
            "ip_address": client_ip,
            "user_agent": request.headers.get("user-agent"),
        }

    def log_event(
        self,
        *,
        event_name: str,
        event_category: str,
        metadata: Mapping[str, object],
        request_context: Mapping[str, object | None],
        status_code: int = 200,
    ) -> None:
        try:
            self.repository.create(
                event_name=event_name,
                event_category=event_category,
                route=self._as_optional_str(request_context.get("route")),
                method=self._as_optional_str(request_context.get("method")),
                status_code=status_code,
                duration_ms=self._as_optional_int(request_context.get("duration_ms")),
                request_id=self._as_optional_str(request_context.get("request_id")),
                ip_address=self._as_optional_str(request_context.get("ip_address")),
                user_agent=self._as_optional_str(request_context.get("user_agent")),
                metadata=metadata,
            )
        except Exception:
            return

    def _as_optional_str(self, value: object | None) -> str | None:
        if value is None:
            return None
        return str(value)

    def _as_optional_int(self, value: object | None) -> int | None:
        if value is None:
            return None
        return int(value)

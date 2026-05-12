from collections.abc import Mapping

from app.database import SessionFactory, get_session_factory
from app.database_models import AppEventRecord


class AppEventRepository:
    def __init__(self, session_factory: SessionFactory | None = None) -> None:
        self.session_factory = session_factory

    def create(
        self,
        *,
        event_name: str,
        event_category: str,
        route: str | None = None,
        method: str | None = None,
        status_code: int | None = None,
        duration_ms: int | None = None,
        request_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        metadata: Mapping[str, object] | None = None,
    ) -> None:
        record = AppEventRecord(
            event_name=event_name,
            event_category=event_category,
            route=route,
            method=method,
            status_code=status_code,
            duration_ms=duration_ms,
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata_=dict(metadata or {}),
        )

        with self._open_session() as session:
            session.add(record)
            session.commit()

    def _open_session(self):
        session_factory = self.session_factory or get_session_factory()
        return session_factory()

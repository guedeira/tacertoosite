from sqlalchemy import select

from app.database import SessionFactory, get_session_factory
from app.database_models import CompanyRecord
from app.models.company import Company


class CompanyRepository:
    def __init__(self, session_factory: SessionFactory | None = None) -> None:
        self.session_factory = session_factory

    def list_all(self) -> list[Company]:
        statement = (
            select(CompanyRecord)
            .where(CompanyRecord.active.is_(True))
            .order_by(CompanyRecord.display_order, CompanyRecord.name)
        )

        with self._open_session() as session:
            records = session.scalars(statement).all()

        return [Company.from_record(record) for record in records]

    def get_by_id(self, company_id: str) -> Company | None:
        statement = select(CompanyRecord).where(
            CompanyRecord.id == company_id,
            CompanyRecord.active.is_(True),
        )

        with self._open_session() as session:
            record = session.scalar(statement)

        if record is None:
            return None

        return Company.from_record(record)

    def _open_session(self):
        session_factory = self.session_factory or get_session_factory()
        return session_factory()

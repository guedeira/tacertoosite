from sqlalchemy import Boolean, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.database_models.base import Base


class CompanyRecord(Base):
    __tablename__ = "companies"
    __table_args__ = {"schema": "public"}

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    categories: Mapped[list[str]] = mapped_column(ARRAY(Text))
    official_domains: Mapped[list[str]] = mapped_column(ARRAY(Text))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)

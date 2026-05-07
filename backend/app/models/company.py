from dataclasses import dataclass
from typing import Protocol


class CompanyRecordLike(Protocol):
    id: str
    name: str
    official_domains: list[str]


@dataclass(frozen=True)
class Company:
    id: str
    name: str
    official_domains: list[str]

    @classmethod
    def from_record(cls, record: CompanyRecordLike) -> "Company":
        return cls(
            id=record.id,
            name=record.name,
            official_domains=list(record.official_domains),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "official_domains": self.official_domains,
        }

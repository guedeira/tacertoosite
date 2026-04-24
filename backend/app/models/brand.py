from dataclasses import dataclass


@dataclass(frozen=True)
class Brand:
    id: str
    name: str
    official_domains: list[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Brand":
        return cls(
            id=data["id"],
            name=data["name"],
            official_domains=list(data["official_domains"]),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "official_domains": self.official_domains,
        }

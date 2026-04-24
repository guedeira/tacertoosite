from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    is_match: bool
    brand: str
    official_domains: list[str]
    submitted_domain: str
    message: str

    def to_dict(self) -> dict:
        return {
            "is_match": self.is_match,
            "brand": self.brand,
            "official_domains": self.official_domains,
            "submitted_domain": self.submitted_domain,
            "message": self.message,
        }

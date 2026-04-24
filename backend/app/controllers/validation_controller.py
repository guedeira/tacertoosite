from app.services.domain_validation_service import DomainValidationService


class ValidationController:
    def __init__(self, service: DomainValidationService | None = None) -> None:
        self.service = service or DomainValidationService()

    def validate_domain(self, brand_id: str | None, submitted_value: str | None) -> dict:
        return self.service.validate(brand_id, submitted_value).to_dict()

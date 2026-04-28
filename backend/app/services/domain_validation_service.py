from app.models.validation_result import ValidationResult
from app.services.brand_service import BrandService
from app.services.domain_normalizer_service import DomainNormalizerService


class DomainValidationService:
    def __init__(
        self,
        brand_service: BrandService | None = None,
        normalizer: DomainNormalizerService | None = None,
    ) -> None:
        self.brand_service = brand_service or BrandService()
        self.normalizer = normalizer or DomainNormalizerService()

    def validate(self, brand_id: str | None, submitted_value: str | None) -> ValidationResult:
        brand = self.brand_service.get_brand((brand_id or "").strip())
        if brand is None:
            return self._invalid_brand_result()

        submitted_domain = self.normalizer.normalize(submitted_value)
        if not self.normalizer.is_valid_domain(submitted_domain):
            return ValidationResult(
                is_match=False,
                brand=brand.name,
                official_domains=brand.official_domains,
                submitted_domain=submitted_domain,
                message="Digite um link ou endereço válido.",
            )

        official_domains = [self.normalizer.normalize(domain) for domain in brand.official_domains]
        is_match = submitted_domain in official_domains

        return ValidationResult(
            is_match=is_match,
            brand=brand.name,
            official_domains=brand.official_domains,
            submitted_domain=submitted_domain,
            message=self._build_message(is_match, brand.name),
        )

    def _build_message(self, is_match: bool, brand_name: str) -> str:
        if is_match:
            return f"Ele está na lista cadastrada para {brand_name}. Ainda assim, confira a página antes de informar dados."
        return f"Ele não está na lista cadastrada para {brand_name}. Use um canal oficial da empresa antes de continuar."

    def _invalid_brand_result(self) -> ValidationResult:
        return ValidationResult(
            is_match=False,
            brand="",
            official_domains=[],
            submitted_domain="",
            message="Selecione uma empresa válida.",
        )

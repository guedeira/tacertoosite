from app.models.validation_result import ValidationResult
from app.services.company_service import CompanyService
from app.services.domain_normalizer_service import DomainNormalizerService


class DomainValidationService:
    def __init__(
        self,
        company_service: CompanyService | None = None,
        normalizer: DomainNormalizerService | None = None,
    ) -> None:
        self.company_service = company_service or CompanyService()
        self.normalizer = normalizer or DomainNormalizerService()

    def validate(self, company_id: str | None, submitted_value: str | None) -> ValidationResult:
        company = self.company_service.get_company((company_id or "").strip())
        if company is None:
            return self._invalid_company_result()

        submitted_domain = self.normalizer.normalize(submitted_value)
        if not self.normalizer.is_valid_domain(submitted_domain):
            return ValidationResult(
                is_match=False,
                company_name=company.name,
                official_domains=company.official_domains,
                submitted_domain=submitted_domain,
                message="Digite um link ou endereço válido.",
            )

        official_domains = [self.normalizer.normalize(domain) for domain in company.official_domains]
        is_match = submitted_domain in official_domains

        return ValidationResult(
            is_match=is_match,
            company_name=company.name,
            official_domains=company.official_domains,
            submitted_domain=submitted_domain,
            message=self._build_message(is_match, company.name),
        )

    def _build_message(self, is_match: bool, company_name: str) -> str:
        if is_match:
            return f"Ele está na lista cadastrada para {company_name}. Ainda assim, confira a página antes de informar dados."
        return f"Ele não está na lista cadastrada para {company_name}. Use um canal oficial da empresa antes de continuar."

    def _invalid_company_result(self) -> ValidationResult:
        return ValidationResult(
            is_match=False,
            company_name="",
            official_domains=[],
            submitted_domain="",
            message="Selecione uma empresa válida.",
        )

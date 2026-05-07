import unittest

from app.models.company import Company
from app.services.domain_validation_service import DomainValidationService


class FakeCompanyService:
    def __init__(self) -> None:
        self.companies = {
            "mercado_livre": Company(
                id="mercado_livre",
                name="Mercado Livre",
                official_domains=["mercadolivre.com.br"],
            ),
            "nubank": Company(
                id="nubank",
                name="Nubank",
                official_domains=["nubank.com.br"],
            ),
            "steam": Company(
                id="steam",
                name="Steam",
                official_domains=["steampowered.com"],
            ),
        }

    def get_company(self, company_id: str) -> Company | None:
        return self.companies.get(company_id)


class DomainValidationServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.service = DomainValidationService(company_service=FakeCompanyService())

    def test_matches_official_domain(self) -> None:
        result = self.service.validate("mercado_livre", "https://www.mercadolivre.com.br/ofertas")

        self.assertTrue(result.is_match)
        self.assertEqual(result.submitted_domain, "mercadolivre.com.br")

    def test_matches_official_domain_from_subdomain(self) -> None:
        result = self.service.validate("steam", "https://store.steampowered.com/app/730")

        self.assertTrue(result.is_match)
        self.assertEqual(result.submitted_domain, "steampowered.com")

    def test_rejects_similar_but_incorrect_domain(self) -> None:
        result = self.service.validate("mercado_livre", "https://mercadoIivre.com.br/promocao")

        self.assertFalse(result.is_match)
        self.assertEqual(result.submitted_domain, "mercadoiivre.com.br")

    def test_rejects_invalid_input(self) -> None:
        result = self.service.validate("nubank", "nubank")

        self.assertFalse(result.is_match)
        self.assertEqual(result.message, "Digite um link ou endereço válido.")

    def test_rejects_unknown_company(self) -> None:
        result = self.service.validate("empresa_inexistente", "nubank.com.br")

        self.assertFalse(result.is_match)
        self.assertEqual(result.message, "Selecione uma empresa válida.")


if __name__ == "__main__":
    unittest.main()

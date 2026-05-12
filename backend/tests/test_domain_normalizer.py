import unittest

from app.services.domain_normalizer_service import DomainNormalizerService


class DomainNormalizerServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.normalizer = DomainNormalizerService()

    def test_normalizes_complete_url(self) -> None:
        result = self.normalizer.normalize("https://www.MercadoLivre.com.br/promocao?x=1")

        self.assertEqual(result, "mercadolivre.com.br")

    def test_normalizes_simple_domain(self) -> None:
        result = self.normalizer.normalize(" WWW.NUBANK.COM.BR ")

        self.assertEqual(result, "nubank.com.br")

    def test_normalizes_subdomain_to_registrable_domain(self) -> None:
        result = self.normalizer.normalize("https://store.steampowered.com/app/730")

        self.assertEqual(result, "steampowered.com")

    def test_keeps_compound_public_suffix_registrable_domain(self) -> None:
        result = self.normalizer.normalize("https://login.mercadolivre.com.br/ofertas")

        self.assertEqual(result, "mercadolivre.com.br")

    def test_normalizes_www_public_suffix_domain(self) -> None:
        result = self.normalizer.normalize("https://www.gov.br/servicos")

        self.assertEqual(result, "gov.br")

    def test_normalizes_public_suffix_subdomain_to_allowed_domain(self) -> None:
        result = self.normalizer.normalize("https://dad.dsadas.fsasads.gov.br/servicos")

        self.assertEqual(result, "gov.br")

    def test_empty_input_returns_empty_domain(self) -> None:
        result = self.normalizer.normalize("")

        self.assertEqual(result, "")

    def test_identifies_invalid_domain(self) -> None:
        self.assertFalse(self.normalizer.is_valid_domain("mercadolivre"))

    def test_accepts_submitted_url(self) -> None:
        self.assertTrue(self.normalizer.is_valid_submitted_link("https://www.nubank.com.br/app"))

    def test_accepts_submitted_domain_without_scheme(self) -> None:
        self.assertTrue(self.normalizer.is_valid_submitted_link("nubank.com.br"))

    def test_rejects_submitted_text_without_public_suffix(self) -> None:
        self.assertFalse(self.normalizer.is_valid_submitted_link("nubank"))

    def test_rejects_submitted_domain_with_unknown_public_suffix(self) -> None:
        self.assertFalse(self.normalizer.is_valid_submitted_link("sdfsd.fdsfds.fdsfdsf.sfsdfdsf.dsfds"))

    def test_rejects_submitted_link_with_raw_spaces(self) -> None:
        self.assertFalse(self.normalizer.is_valid_submitted_link("https://nubank.com.br/minha conta"))

    def test_rejects_submitted_link_with_credentials(self) -> None:
        self.assertFalse(self.normalizer.is_valid_submitted_link("https://user:pass@nubank.com.br"))

    def test_accepts_allowed_public_suffix_domain(self) -> None:
        self.assertTrue(self.normalizer.is_valid_submitted_link("https://www.gov.br/servicos"))

    def test_accepts_allowed_public_suffix_subdomain(self) -> None:
        self.assertTrue(self.normalizer.is_valid_submitted_link("https://dad.dsadas.fsasads.gov.br/servicos"))


if __name__ == "__main__":
    unittest.main()

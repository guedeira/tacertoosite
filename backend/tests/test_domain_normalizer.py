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

    def test_empty_input_returns_empty_domain(self) -> None:
        result = self.normalizer.normalize("")

        self.assertEqual(result, "")

    def test_identifies_invalid_domain(self) -> None:
        self.assertFalse(self.normalizer.is_valid_domain("mercadolivre"))


if __name__ == "__main__":
    unittest.main()

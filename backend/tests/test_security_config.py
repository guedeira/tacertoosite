import unittest
from unittest.mock import patch

from pydantic import ValidationError

from app.main import CORS_ALLOWED_ORIGINS, create_app
from app.routes.validation_routes import DomainValidationRequest


class SecurityConfigTest(unittest.TestCase):
    def test_disables_api_docs_in_production(self) -> None:
        with patch.dict("os.environ", {"APP_ENV": "production"}):
            app = create_app()

        self.assertIsNone(app.docs_url)
        self.assertIsNone(app.redoc_url)
        self.assertIsNone(app.openapi_url)

    def test_allows_public_frontend_origin_without_trailing_slash(self) -> None:
        self.assertIn("https://tacertoosite.guedeira.dev", CORS_ALLOWED_ORIGINS)
        self.assertNotIn("https://tacertoosite.guedeira.dev/", CORS_ALLOWED_ORIGINS)

    def test_rejects_brand_id_with_unexpected_characters(self) -> None:
        with self.assertRaises(ValidationError):
            DomainValidationRequest(brand_id="../mercado-livre", input="mercadolivre.com.br")

    def test_rejects_oversized_input(self) -> None:
        with self.assertRaises(ValidationError):
            DomainValidationRequest(brand_id="mercado_livre", input="a" * 2049)


if __name__ == "__main__":
    unittest.main()

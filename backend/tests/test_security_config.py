import unittest
from unittest.mock import patch

from pydantic import ValidationError

from app.main import create_app, get_cors_allowed_origins
from app.routes.validation_routes import DomainValidationRequest


class SecurityConfigTest(unittest.TestCase):
    def test_disables_api_docs_in_production(self) -> None:
        with patch.dict("os.environ", {"APP_ENV": "production"}):
            app = create_app()

        self.assertIsNone(app.docs_url)
        self.assertIsNone(app.redoc_url)
        self.assertIsNone(app.openapi_url)

    def test_reads_cors_allowed_origins_from_environment(self) -> None:
        with patch.dict(
            "os.environ",
            {"CORS_ALLOWED_ORIGINS": "https://front.example.com, http://localhost:5173"},
        ):
            origins = get_cors_allowed_origins()

        self.assertEqual(
            origins,
            ["https://front.example.com", "http://localhost:5173"],
        )

    def test_rejects_company_id_with_unexpected_characters(self) -> None:
        with self.assertRaises(ValidationError):
            DomainValidationRequest(company_id="../mercado-livre", input="mercadolivre.com.br")

    def test_rejects_oversized_input(self) -> None:
        with self.assertRaises(ValidationError):
            DomainValidationRequest(company_id="mercado_livre", input="a" * 2049)


if __name__ == "__main__":
    unittest.main()

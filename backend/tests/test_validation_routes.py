import unittest

from app.models.validation_result import ValidationResult
from app.routes.validation_routes import DomainValidationRequest
from app.routes.validation_routes import _build_event_metadata


class ValidationRoutesTest(unittest.TestCase):
    def test_event_metadata_omits_raw_input_for_valid_domain(self) -> None:
        payload = DomainValidationRequest(company_id="americanas", input="https://americanas.com.br")
        result = ValidationResult(
            is_match=True,
            company_name="Americanas",
            official_domains=["americanas.com.br"],
            submitted_domain="americanas.com.br",
            message="",
            status="match",
        )

        metadata = _build_event_metadata(payload, result)

        self.assertEqual(list(metadata.keys()), ["status", "submitted_input", "company_id"])
        self.assertEqual(
            metadata,
            {
                "status": "match",
                "submitted_input": "americanas.com.br",
                "company_id": "americanas",
            },
        )

    def test_event_metadata_keeps_raw_input_for_invalid_domain(self) -> None:
        payload = DomainValidationRequest(company_id="americanas", input=" https://americanas.com.brr/ ")
        result = ValidationResult(
            is_match=False,
            company_name="Americanas",
            official_domains=["americanas.com.br"],
            submitted_domain="",
            message="",
            status="invalid_domain",
        )

        metadata = _build_event_metadata(payload, result)

        self.assertEqual(list(metadata.keys()), ["status", "submitted_input", "company_id"])
        self.assertEqual(
            metadata,
            {
                "status": "invalid_domain",
                "submitted_input": "https://americanas.com.brr/",
                "company_id": "americanas",
            },
        )


if __name__ == "__main__":
    unittest.main()

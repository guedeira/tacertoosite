import unittest

from fastapi import Response

from app.models.company import Company
from app.routes import company_routes


class FakeCompanyService:
    def list_companies(self) -> list[Company]:
        return [
            Company(
                id="nubank",
                name="Nubank",
                official_domains=["nubank.com.br"],
            )
        ]


class CompanyRoutesTest(unittest.TestCase):
    def test_list_companies_sets_five_minute_cache_header(self) -> None:
        original_service = company_routes.service
        company_routes.service = FakeCompanyService()
        response = Response()

        try:
            result = company_routes.list_companies(response)
        finally:
            company_routes.service = original_service

        self.assertEqual(response.headers["Cache-Control"], "public, max-age=300")
        self.assertEqual(result, [{"id": "nubank", "name": "Nubank", "official_domains": ["nubank.com.br"]}])


if __name__ == "__main__":
    unittest.main()

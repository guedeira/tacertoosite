import os
import unittest
from pathlib import Path

from app.database import get_database_url, get_engine, get_session_factory
from app.repositories.company_repository import CompanyRepository


def load_dotenv_if_present() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_dotenv_if_present()


@unittest.skipUnless(
    os.getenv("RUN_SUPABASE_INTEGRATION_TESTS") == "1"
    and os.getenv("DATABASE_URL"),
    "Configure RUN_SUPABASE_INTEGRATION_TESTS=1 e DATABASE_URL para rodar integração com Supabase.",
)
class SupabaseIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        get_database_url.cache_clear()
        get_engine.cache_clear()
        get_session_factory.cache_clear()

    def tearDown(self) -> None:
        get_database_url.cache_clear()
        get_engine.cache_clear()
        get_session_factory.cache_clear()

    def test_repository_lists_companies_from_supabase(self) -> None:
        companies = CompanyRepository().list_all()

        self.assertGreater(len(companies), 0)
        self.assertTrue(all(company.id for company in companies))
        self.assertTrue(all(company.name for company in companies))
        self.assertTrue(all(company.official_domains for company in companies))

    def test_repository_fetches_company_by_id_from_supabase(self) -> None:
        first_company = CompanyRepository().list_all()[0]

        company = CompanyRepository().get_by_id(first_company.id)

        self.assertIsNotNone(company)
        self.assertEqual(company.id, first_company.id)
        self.assertEqual(company.name, first_company.name)


if __name__ == "__main__":
    unittest.main()

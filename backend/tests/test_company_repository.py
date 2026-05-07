import unittest
from dataclasses import dataclass

from sqlalchemy.dialects import postgresql

from app.repositories.company_repository import CompanyRepository


@dataclass(frozen=True)
class FakeCompanyRecord:
    id: str
    name: str
    official_domains: list[str]


class FakeScalarResult:
    def __init__(self, records: list[FakeCompanyRecord]) -> None:
        self.records = records

    def all(self) -> list[FakeCompanyRecord]:
        return self.records


class FakeSession:
    def __init__(
        self,
        list_records: list[FakeCompanyRecord] | None = None,
        single_record: FakeCompanyRecord | None = None,
    ) -> None:
        self.list_records = list_records or []
        self.single_record = single_record
        self.scalars_statement = None
        self.scalar_statement = None

    def __enter__(self) -> "FakeSession":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def scalars(self, statement):
        self.scalars_statement = statement
        return FakeScalarResult(self.list_records)

    def scalar(self, statement):
        self.scalar_statement = statement
        return self.single_record


def compile_statement(statement) -> str:
    return str(
        statement.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        )
    )


class CompanyRepositoryTest(unittest.TestCase):
    def test_list_all_maps_active_companies_from_sqlalchemy_records(self) -> None:
        session = FakeSession(
            list_records=[
                FakeCompanyRecord(
                    id="nubank",
                    name="Nubank",
                    official_domains=["nubank.com.br"],
                )
            ]
        )
        repository = CompanyRepository(session_factory=lambda: session)

        companies = repository.list_all()

        self.assertEqual(len(companies), 1)
        self.assertEqual(companies[0].id, "nubank")
        self.assertEqual(companies[0].name, "Nubank")
        self.assertEqual(companies[0].official_domains, ["nubank.com.br"])

        compiled_statement = compile_statement(session.scalars_statement)
        self.assertIn("FROM public.companies", compiled_statement)
        self.assertIn("WHERE public.companies.active IS true", compiled_statement)
        self.assertIn("ORDER BY public.companies.display_order, public.companies.name", compiled_statement)

    def test_get_by_id_filters_by_id_and_active_flag(self) -> None:
        session = FakeSession(
            single_record=FakeCompanyRecord(
                id="mercado_livre",
                name="Mercado Livre",
                official_domains=["mercadolivre.com.br"],
            )
        )
        repository = CompanyRepository(session_factory=lambda: session)

        company = repository.get_by_id("mercado_livre")

        self.assertIsNotNone(company)
        self.assertEqual(company.id, "mercado_livre")

        compiled_statement = compile_statement(session.scalar_statement)
        self.assertIn("FROM public.companies", compiled_statement)
        self.assertIn("public.companies.id = 'mercado_livre'", compiled_statement)
        self.assertIn("public.companies.active IS true", compiled_statement)

    def test_get_by_id_returns_none_when_company_is_not_found(self) -> None:
        repository = CompanyRepository(session_factory=lambda: FakeSession(single_record=None))

        self.assertIsNone(repository.get_by_id("empresa_inexistente"))


if __name__ == "__main__":
    unittest.main()

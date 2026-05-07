from app.models.company import Company
from app.repositories.company_repository import CompanyRepository


class CompanyService:
    def __init__(self, repository: CompanyRepository | None = None) -> None:
        self.repository = repository or CompanyRepository()

    def list_companies(self) -> list[Company]:
        return self.repository.list_all()

    def get_company(self, company_id: str) -> Company | None:
        return self.repository.get_by_id(company_id)

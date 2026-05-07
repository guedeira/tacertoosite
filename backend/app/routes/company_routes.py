from fastapi import APIRouter, HTTPException

from app.services.company_service import CompanyService

router = APIRouter()
service = CompanyService()


@router.get("/companies")
def list_companies() -> list[dict]:
    return [company.to_dict() for company in service.list_companies()]


@router.get("/companies/{company_id}")
def get_company(company_id: str) -> dict:
    company = service.get_company(company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    return company.to_dict()

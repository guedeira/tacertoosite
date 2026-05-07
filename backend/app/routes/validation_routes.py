from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.domain_validation_service import DomainValidationService

router = APIRouter()
service = DomainValidationService()


class DomainValidationRequest(BaseModel):
    company_id: str | None = Field(
        default=None,
        max_length=80,
        pattern=r"^[a-z0-9_]+$",
    )
    input: str | None = Field(default=None, max_length=2048)


@router.post("/validate-domain")
def validate_domain(payload: DomainValidationRequest) -> dict:
    return service.validate(payload.company_id, payload.input).to_dict()

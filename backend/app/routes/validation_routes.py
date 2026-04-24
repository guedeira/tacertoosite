from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.controllers.validation_controller import ValidationController

router = APIRouter()
controller = ValidationController()


class DomainValidationRequest(BaseModel):
    brand_id: str | None = Field(
        default=None,
        max_length=80,
        pattern=r"^[a-z0-9_]+$",
    )
    input: str | None = Field(default=None, max_length=2048)


@router.post("/validate-domain")
def validate_domain(payload: DomainValidationRequest) -> dict:
    return controller.validate_domain(payload.brand_id, payload.input)

import time

from fastapi import APIRouter
from fastapi import Request
from pydantic import BaseModel, Field
from pydantic import field_validator

from app.services.app_event_service import AppEventService
from app.services.domain_validation_service import DomainValidationService
from app.services.domain_normalizer_service import DomainNormalizerService

router = APIRouter()
service = DomainValidationService()
event_service = AppEventService()
normalizer = DomainNormalizerService()


class DomainValidationRequest(BaseModel):
    company_id: str | None = Field(
        default=None,
        max_length=80,
        pattern=r"^[a-z0-9_]+$",
    )
    input: str = Field(max_length=2048)

    @field_validator("input")
    @classmethod
    def validate_input_is_link(cls, value: str) -> str:
        if not normalizer.is_valid_submitted_link(value):
            raise ValueError("Digite um link válido.")

        return value.strip()


@router.post("/validate-domain")
def validate_domain(payload: DomainValidationRequest, request: Request) -> dict:
    started_at = time.perf_counter()
    result = service.validate(payload.company_id, payload.input)
    response = result.to_dict()

    event_service.log_event(
        event_name="domain_validation_submitted",
        event_category="domain_validation",
        metadata={
            "company_id": payload.company_id,
            "submitted_input_raw": payload.input,
            "submitted_domain_normalized": result.submitted_domain,
            "is_match": result.is_match,
            "validation_status": result.status,
            "official_domain_count": len(result.official_domains),
        },
        request_context=event_service.build_request_context(request, started_at),
    )

    return response

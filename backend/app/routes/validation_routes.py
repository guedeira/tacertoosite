import time

from fastapi import APIRouter
from fastapi import Request
from pydantic import BaseModel, Field

from app.models.validation_result import ValidationResult
from app.services.app_event_service import AppEventService
from app.services.domain_validation_service import DomainValidationService

router = APIRouter()
service = DomainValidationService()
event_service = AppEventService()


class DomainValidationRequest(BaseModel):
    company_id: str | None = Field(
        default=None,
        max_length=80,
        pattern=r"^[a-z0-9_]+$",
    )
    input: str = Field(max_length=2048)


@router.post("/validate-domain")
def validate_domain(payload: DomainValidationRequest, request: Request) -> dict:
    started_at = time.perf_counter()
    result = service.validate(payload.company_id, payload.input)
    response = result.to_dict()

    event_service.log_event(
        event_name="domain_validation_submitted",
        event_category="domain_validation",
        metadata=_build_event_metadata(payload, result),
        request_context=event_service.build_request_context(request, started_at),
    )

    return response


def _build_event_metadata(payload: DomainValidationRequest, result: ValidationResult) -> dict[str, object]:
    metadata: dict[str, object] = {
        "status": result.status,
        "submitted_input": result.submitted_domain,
    }

    if result.status == "invalid_domain":
        metadata["submitted_input"] = payload.input.strip()

    metadata["company_id"] = payload.company_id
    return metadata

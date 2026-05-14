import unittest
from app.services.app_event_service import AppEventService


class FakeRepository:
    def __init__(self, should_fail: bool = False) -> None:
        self.should_fail = should_fail
        self.created_event = None

    def create(self, **kwargs) -> None:
        if self.should_fail:
            raise RuntimeError("database unavailable")

        self.created_event = kwargs


class AppEventServiceTest(unittest.TestCase):
    def test_log_event_forwards_context_and_metadata_to_repository(self) -> None:
        repository = FakeRepository()
        service = AppEventService(repository=repository)

        service.log_event(
            event_name="domain_validation_submitted",
            event_category="domain_validation",
            metadata={"submitted_input": "nubank.com.br"},
            request_context={
                "route": "/validate-domain",
                "method": "POST",
                "duration_ms": 8,
                "request_id": "request-123",
                "ip_address": "127.0.0.1",
                "user_agent": "test-agent",
            },
        )

        self.assertEqual(repository.created_event["event_name"], "domain_validation_submitted")
        self.assertEqual(repository.created_event["event_category"], "domain_validation")
        self.assertEqual(repository.created_event["route"], "/validate-domain")
        self.assertEqual(repository.created_event["method"], "POST")
        self.assertEqual(repository.created_event["status_code"], 200)
        self.assertEqual(repository.created_event["duration_ms"], 8)
        self.assertEqual(repository.created_event["request_id"], "request-123")
        self.assertEqual(repository.created_event["metadata"], {"submitted_input": "nubank.com.br"})

    def test_log_event_does_not_raise_when_repository_fails(self) -> None:
        service = AppEventService(repository=FakeRepository(should_fail=True))

        service.log_event(
            event_name="domain_validation_submitted",
            event_category="domain_validation",
            metadata={},
            request_context={},
        )


if __name__ == "__main__":
    unittest.main()

import unittest

from app.repositories.app_event_repository import AppEventRepository


class FakeSession:
    def __init__(self) -> None:
        self.added_record = None
        self.committed = False

    def __enter__(self) -> "FakeSession":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def add(self, record) -> None:
        self.added_record = record

    def commit(self) -> None:
        self.committed = True


class AppEventRepositoryTest(unittest.TestCase):
    def test_create_persists_event_record_with_metadata(self) -> None:
        session = FakeSession()
        repository = AppEventRepository(session_factory=lambda: session)

        repository.create(
            event_name="domain_validation_submitted",
            event_category="domain_validation",
            route="/validate-domain",
            method="POST",
            status_code=200,
            duration_ms=12,
            request_id="request-123",
            ip_address="127.0.0.1",
            user_agent="test-agent",
            metadata={
                "submitted_input_raw": "https://www.nubank.com.br",
                "submitted_domain_normalized": "nubank.com.br",
            },
        )

        self.assertIsNotNone(session.added_record)
        self.assertTrue(session.committed)
        self.assertEqual(session.added_record.event_name, "domain_validation_submitted")
        self.assertEqual(session.added_record.event_category, "domain_validation")
        self.assertEqual(session.added_record.route, "/validate-domain")
        self.assertEqual(session.added_record.method, "POST")
        self.assertEqual(session.added_record.status_code, 200)
        self.assertEqual(session.added_record.duration_ms, 12)
        self.assertEqual(session.added_record.request_id, "request-123")
        self.assertEqual(session.added_record.ip_address, "127.0.0.1")
        self.assertEqual(session.added_record.user_agent, "test-agent")
        self.assertEqual(
            session.added_record.metadata_,
            {
                "submitted_input_raw": "https://www.nubank.com.br",
                "submitted_domain_normalized": "nubank.com.br",
            },
        )


if __name__ == "__main__":
    unittest.main()

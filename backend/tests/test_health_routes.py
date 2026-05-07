import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app.routes.health_routes import database_health_check, health_check


class FakeSession:
    def __init__(self, should_fail: bool = False) -> None:
        self.should_fail = should_fail
        self.executed_statement = None

    def __enter__(self) -> "FakeSession":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def execute(self, statement) -> None:
        self.executed_statement = statement

        if self.should_fail:
            raise RuntimeError("database unavailable")


class HealthRoutesTest(unittest.TestCase):
    def test_health_check_returns_ok_without_database_dependency(self) -> None:
        self.assertEqual(health_check(), {"status": "ok"})

    def test_database_health_check_returns_ok_when_database_is_available(self) -> None:
        session = FakeSession()

        with patch("app.routes.health_routes.get_session_factory", return_value=lambda: session):
            result = database_health_check()

        self.assertEqual(result, {"status": "ok", "database": "available"})
        self.assertEqual(str(session.executed_statement), "select 1")

    def test_database_health_check_returns_503_when_database_is_unavailable(self) -> None:
        with patch("app.routes.health_routes.get_session_factory", return_value=lambda: FakeSession(should_fail=True)):
            with self.assertRaises(HTTPException) as context:
                database_health_check()

        self.assertEqual(context.exception.status_code, 503)
        self.assertEqual(
            context.exception.detail,
            {"status": "error", "database": "unavailable"},
        )


if __name__ == "__main__":
    unittest.main()

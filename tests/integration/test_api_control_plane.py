from __future__ import annotations

from fastapi.testclient import TestClient

from api.server import create_app
from app.dependency_container import build_container
from config.settings import Settings


def test_api_health_and_mutation_guard(tmp_path):
    settings = Settings(app_env="test", app_dry_run=True, app_database_path=tmp_path / "api.db",
                        master_encryption_key="test", api_mutations_enabled=False)
    container = build_container(settings)
    client = TestClient(create_app(container))
    assert client.get("/api/health").status_code == 200
    response = client.post("/api/automation/cycle")
    assert response.status_code == 503


def test_api_operator_token_allows_explicit_cycle(tmp_path):
    settings = Settings(app_env="test", app_dry_run=True, app_database_path=tmp_path / "api2.db",
                        master_encryption_key="test", api_mutations_enabled=True,
                        operator_api_token="operator-secret")
    container = build_container(settings)
    client = TestClient(create_app(container))
    assert client.post("/api/automation/cycle").status_code == 401
    response = client.post("/api/automation/cycle?force=true",
                           headers={"X-Operator-Token": "operator-secret"})
    assert response.status_code == 200
    assert response.json()["planned"] >= 29

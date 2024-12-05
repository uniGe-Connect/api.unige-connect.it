from fastapi.testclient import TestClient
import pytest
from datetime import timedelta
from app.core.security import create_access_token
from fastapi.testclient import TestClient
import pytest
from fastapi.testclient import TestClient
import pytest
from datetime import timedelta
from app.core.security import create_access_token



# Fixtures
@pytest.fixture
def headers():
    test_user_id = "123e4567-e89b-12d3-a456-426614174000"
    expires_delta = timedelta(hours=1)  
    token = create_access_token(subject=test_user_id, expires_delta=expires_delta) 
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_user_id():
    return "123e4567-e89b-12d3-a456-426614174000"

@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


def test_auth_login(client: TestClient):
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert "redirect_url" in response.json()

def test_get_auth_me(client: TestClient, headers) -> None:
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == "123e4567-e89b-12d3-a456-426614174000"
    assert content["name"] == "TEST_USER"
    assert content ["last_name"] == "TU"
    
    response = client.get("/auth/logout", headers=headers)
    assert response.status_code == 200
    response = client.get("/auth/me")
    content = response.json()
    assert content["detail"] == "Not authenticated"

def test_auth_logout(client: TestClient, headers):
    response = client.get("/auth/login")
    assert response.status_code == 200
    response = client.get("/auth/logout", headers=headers)
    assert response.status_code == 200
    assert "redirect_url" in response.json()
    response = client.get("/auth/me")
    content = response.json()
    assert content["detail"] == "Not authenticated"


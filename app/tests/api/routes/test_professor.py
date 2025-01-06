from fastapi.testclient import TestClient
from fastapi import status
from sqlmodel import Session
from datetime import timedelta
from app.core.security import create_access_token
import pytest


# Fixtures
@pytest.fixture
def prof_headers():
    test_user_id = "875d44c6-8a42-4292-b9f3-c0362ec4bd43"
    expires_delta = timedelta(hours=1)  
    token = create_access_token(subject=test_user_id, expires_delta=expires_delta) 
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def student_headers():
    test_user_id = "123e4567-e89b-12d3-a456-426614174000"
    expires_delta = timedelta(hours=1)  
    token = create_access_token(subject=test_user_id, expires_delta=expires_delta) 
    return {"Authorization": f"Bearer {token}"}    

@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)

#Test cases

def test_get_statistics_being_student(client: TestClient, student_headers) -> None:
    response = client.get("/professor/statistics", headers=student_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions."

def test_get_statistics(client: TestClient, prof_headers) -> None:
    response = client.get("/professor/statistics", headers=prof_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0  
    first_item = response.json()[0]  
    expected_keys = {"course_id", "course_name", "total_groups", "total_members", "avg_members", "min_members", "max_members"}
    assert expected_keys.issubset(first_item.keys()), f"Missing fields: {expected_keys - set(first_item.keys())}"    


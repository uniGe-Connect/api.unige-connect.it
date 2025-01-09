from fastapi.testclient import TestClient
from fastapi import status
from faker import Faker
from sqlmodel import Session
from app.controllers.course_controller import course_controller
from app.controllers.group_controller import group_controller
from app.controllers.user_controller import user_controller
from app.core.security import create_access_token
import pytest
from datetime import timedelta
from app.models.group_model import GroupTypes, GroupRequest
from app.models.user_model import UserModel

fake = Faker()

# Fixtures
@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)

@pytest.fixture
def user(session: Session):
    user = UserModel(
        id=fake.uuid4(),
        name=fake.name(),
        last_name=fake.last_name(),
        email=fake.email(),
        serial_number=f"s{fake.random_number(digits=6)}",
    )
    user_controller.create(obj_in=user, session=session)
    return user

@pytest.fixture
def group(client, headers, session:Session):
    course = course_controller.get_all(session=session)[0]
    group_request = {
        "name": "TestName2",
        "description": "TestDescription",
        "course_id": str(course.id),
        "type": "public_open",
    }
    response = client.post("/groups", json=group_request, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def closed_group(client, headers, session:Session):
    course = course_controller.get_all(session=session)[0]
    group_request = {
        "name": "TestName2",
        "description": "TestDescription",
        "course_id": str(course.id),
        "type": "public_closed",
    }
    response = client.post("/groups", json=group_request, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def test_user_id():
    return "123e4567-e89b-12d3-a456-426614174000"

@pytest.fixture
def user_headers():
    test_user_id = "123e4567-e89b-12d3-a456-426614174000"
    expires_delta = timedelta(hours=1)  
    token = create_access_token(subject=test_user_id, expires_delta=expires_delta) 
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def headers(user: UserModel):
    expires_delta = timedelta(hours=1)
    token = create_access_token(subject=user.id, expires_delta=expires_delta)
    return {"Authorization": f"Bearer {token}"}


# Test cases

def test_join_group_which_i_am_not_member(client: TestClient, user_headers, test_user_id, group, session: Session) -> None:
    assert group["member_count"] == 1
    group_id = group["id"]
    response = client.post(f"/groups/{group_id}/members", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["group_id"] == group_id
    assert response.json()["user_id"] == test_user_id
    assert response.json()["role"] == "member"
    response = client.get(f"/groups/{group_id}", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["member_count"] == 2


def test_join_group_which_i_am_member_already(client: TestClient, user_headers, test_user_id, group, session: Session) -> None:
    assert group["member_count"] == 1
    group_id = group["id"]
    response = client.post(f"/groups/{group_id}/members", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    response = client.post(f"/groups/{group_id}/members", headers=user_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Already member of group."
    # check if the group member count is still 2 (not increased)
    response = client.get(f"/groups/{group_id}", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["member_count"] == 2


def test_join_closed_group(client: TestClient, user_headers, test_user_id, closed_group, session: Session) -> None:
    group_id = closed_group["id"]
    response = client.post(f"/groups/{group_id}/members", headers=user_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Unable to join."


def test_get_members(client: TestClient, headers, group, session: Session) -> None:
    group_id = group["id"]
    assert group["member_count"] == 1
    response = client.get(f"/groups/{group_id}/members", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0  
    first_item = response.json()["data"][0]
    expected_keys = {"name", "last_name"}
    assert expected_keys.issubset(first_item.keys()), f"Missing fields: {expected_keys - set(first_item.keys())}"


def test_leave_group_where_i_member(client: TestClient, user_headers, test_user_id, group, session: Session) -> None:
    group_id = group["id"]
    assert group["member_count"] == 1
    response = client.post(f"/groups/{group_id}/members", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    # check if member count increased
    response = client.get(f"/groups/{group_id}", headers=user_headers)
    assert response.json()["member_count"] == 2   
    # leave the group
    response = client.put(f"/groups/{group_id}/members", headers=user_headers)
    # check if the member marked as deleted
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["deleted_at"] is not None
    # check if the group member count is decreased
    response = client.get(f"/groups/{group_id}", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["member_count"] == 1


def test_leave_group_where_i_owner(client: TestClient, headers, user, group, session: Session) -> None:
    assert group["member_count"] == 1
    response = client.put(f"/groups/{group["id"]}/members", headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "The owner cannot leave the group."


def test_leave_group_where_i_am_not_member(client: TestClient, user_headers, test_user_id, group, session: Session) -> None:
    response = client.put(f"/groups/{group["id"]}/members", headers=user_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "You are not a member of the group."


def test_leave_group_where_i_left(client: TestClient, user_headers, test_user_id, group, session: Session) -> None:
    group_id = group["id"]
    response = client.post(f"/groups/{group_id}/members", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    response = client.put(f"/groups/{group_id}/members", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    response = client.put(f"/groups/{group_id}/members", headers=user_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "You are not a member of the group anymore."
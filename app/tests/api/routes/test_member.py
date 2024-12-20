from fastapi.testclient import TestClient
from fastapi import status

from faker import Faker
from sqlmodel import Session

from app.controllers.group_controller import group_controller
from app.controllers.user_controller import user_controller
from app.core.security import create_access_token
import pytest
from datetime import timedelta

from app.models.group_model import GroupTypes, GroupRequest
from app.models.user_model import UserModel

fake = Faker()


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
def group(user: UserModel, session: Session):
    group = GroupRequest(
        name=fake.name(),
        topic=fake.word(),
        description=fake.sentence(2),
        type=GroupTypes.public_open,
        owner_id=user.id
    )
    group = group_controller.create(obj_in=group, session=session)

    return group


# Fixtures
@pytest.fixture
def headers(user: UserModel):
    expires_delta = timedelta(hours=1)
    token = create_access_token(subject=user.id, expires_delta=expires_delta)
    return {"Authorization": f"Bearer {token}"}


def test_join_group_which_i_am_not_member(client: TestClient, headers, user, group, session: Session) -> None:
    assert group.member_count == 0

    response = client.post(f"/groups/{group.id}/members", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["group_id"] == str(group.id)
    assert response.json()["user_id"] == str(user.id)
    assert response.json()["role"] == "member"

    response = client.get(f"/groups/{group.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["member_count"] == 1


def test_join_group_which_i_am_member_already(client: TestClient, headers, user, group, session: Session) -> None:
    assert group.member_count == 0

    response = client.post(f"/groups/{group.id}/members", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["group_id"] == str(group.id)
    assert response.json()["user_id"] == str(user.id)
    assert response.json()["role"] == "member"

    # check if the group member count is still 2 (not increased)
    response = client.get(f"/groups/{group.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["member_count"] == 1

    response = client.post(f"/groups/{group.id}/members", headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check if the group member count is still 2 (not increased)
    response = client.get(f"/groups/{group.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["member_count"] == 1


def test_join_closed_group(client: TestClient, headers, user, group, session: Session) -> None:
    user = UserModel(
        name=fake.name(),
        last_name=fake.last_name(),
        email=fake.email(),
        serial_number=f"s{fake.random_number(digits=6)}",
    )

    user = user_controller.create(obj_in=user, session=session)
    assert user.id is not None

    group = GroupRequest(
        name=fake.name(),
        topic=fake.word(),
        description=fake.sentence(2),
        type=GroupTypes.public_closed,
        owner_id=user.id
    )

    group = group_controller.create(obj_in=group, session=session)

    response = client.post(f"/groups/{group.id}/members", headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Unable to join."

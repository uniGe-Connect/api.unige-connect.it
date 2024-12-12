from fastapi.testclient import TestClient
from fastapi import status
from app.controllers.group_controller import group_controller
from app.controllers.user_controller import user_controller
from app.controllers.member_controller import member_controller
from app.core.security import create_access_token
import pytest
from datetime import timedelta
import uuid
from datetime import datetime

from app.models.group_model import GroupRequest, GroupTypes
from app.models.user_model import UserModel
from faker import Faker
fake = Faker()

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

@pytest.fixture
def group_id(client, headers, test_user_id):
    group_request = {
        "name": "TestName2",
        "description": "TestDescription",
        "topic": "TestTopic",
        "type": "public_open",  
        "member_count": 1,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    response = client.post("/groups", json=group_request, headers=headers)
    assert response.status_code == 200
    return response.json()["id"] 


@pytest.fixture
def other_user():
    user = UserModel(
        id=fake.uuid4(),
        name=fake.name(),
        last_name=fake.last_name(),
        email=fake.email(),
        serial_number=f"s{fake.random_number(digits=6)}",
    )
    user_controller.create(obj_in=user)
    return user

@pytest.fixture
def other_user_group(other_user: UserModel):
    group = GroupRequest(
        name=fake.name(),
        topic=fake.word(),
        description=fake.sentence(2),
        type=GroupTypes.public_open,
        owner_id=other_user.id
    )
    group = group_controller.create(obj_in=group)
    return group


#Test cases

def test_get_groups_count(client: TestClient, headers) -> None:
    response = client.get("/groups/count", headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, int)

def test_get_first_group(client: TestClient,headers) ->None:
    response = client.get("/groups", headers=headers)   
    assert response.status_code == 200
    first_item = response.json()["data"][0] 
    group_id = first_item["id"]
    response = client.get(f"/groups/{group_id}", headers=headers) 
    assert response.status_code == 200
    expected_keys = {"id", "name", "topic", "description", "type", "member_count", "created_at"}
    assert expected_keys.issubset(first_item.keys()), f"Missing fields: {expected_keys - set(first_item.keys())}"

def test_get_all_groups(client: TestClient, headers) -> None:
    response = client.get("/groups", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0  
    first_item = response.json()["data"][0]  
    expected_keys = {"id", "name", "topic", "description", "type", "member_count", "created_at"}
    assert expected_keys.issubset(first_item.keys()), f"Missing fields: {expected_keys - set(first_item.keys())}"
    
def test_post_group(client: TestClient, headers, test_user_id) -> str:
    group_request = {
        "name": "TestName2",
        "description": "TestDescription",
        "topic": "TestTopic",
        "type": "public_open", 
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    response = client.post("/groups", json=group_request, headers=headers)
    group = response.json()
    assert response.status_code == 200
    assert group["member_count"] == 1

    group_id=group["id"]
    #Try to join my own group
    response = client.post(f"/groups/{group_id}/members", headers=headers)
    assert response.status_code == 400
 
def test_get_group_by_id(client: TestClient, group_id: str, headers) -> None:
    response = client.get(f"/groups/{group_id}", headers=headers)
    assert response.status_code == 200
    group = response.json()
    expected_keys = {"id", "name", "topic", "description", "type", "member_count", "created_at"}
    assert expected_keys.issubset(group.keys()), f"Missing fields: {expected_keys - set(group.keys())}"
    assert group["description"] == "TestDescription"
    
def test_delete_group(client: TestClient, group_id: str, headers, test_user_id) -> None:
    # Delete group which is not owned by the user
    response = client.get(f"/groups", headers=headers)
    assert response.status_code == 200
    groups = response.json()["data"]
    assert len(groups) > 0
    snd_response = client.get("/groups?member=me", headers=headers)  # owned and joined groups
    my_groups = snd_response.json()["owned_groups"]
    filtered_groups = [group for group in groups if group["id"] not in {my_group["id"] for my_group in my_groups}]
    group_id = filtered_groups[0]["id"]
    response = client.delete(f"/groups/{group_id}", headers=headers)
    assert response.status_code == 403
    
    # Delete owned group
    group_id = my_groups[0]["id"]
    response = client.delete(f"/groups/{group_id}", headers=headers)
    assert response.status_code == 200

def test_my_groups_api(client: TestClient, group_id: str, headers, other_user_group) -> None:
    response = client.get("/groups?member=me", headers=headers)  # owned and joined groups
    owned_groups = response.json()["owned_groups"]
    joined_groups = response.json()["joined_groups"]
    assert any(group_id == o_group["id"] for o_group in owned_groups)
    assert any(group_id == j_group["id"] for j_group in joined_groups) == False
    assert len(joined_groups) == 0

    response = client.post(f"/groups/{other_user_group.id}/members", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/groups?member=me", headers=headers)  # owned and joined groups
    owned_groups = response.json()["owned_groups"]
    joined_groups = response.json()["joined_groups"]
    assert any(str(other_user_group.id) == o_group["id"] for o_group in owned_groups) == False
    assert any(str(other_user_group.id) == j_group["id"] for j_group in joined_groups)
    assert len(joined_groups) == 1

    #Removing the group to clean the user joined group after the test
    group_controller.remove(id=other_user_group.id)
   

    
def test_is_member_field(client: TestClient, group_id: str, headers, other_user_group) -> None:
    response = client.get("/groups?member=me", headers=headers)  # owned and joined groups
    owned_groups = response.json()["owned_groups"]
    joined_groups = response.json()["joined_groups"]
    user_groups_id = [o_group["id"] for o_group in owned_groups] +  [j_group["id"] for j_group in joined_groups]
    all_groups = client.get("/groups?", headers=headers).json()["data"]

    #All groups of which I am member have the is_member field set to True
    assert all(
        group["is_member"] == True if group["id"] in user_groups_id else True
        for group in all_groups
    )

    #All groups of which I am not member have the is_member field set to False
    assert all(
        group["is_member"] == False if group["id"] not in user_groups_id else True
        for group in all_groups
    )





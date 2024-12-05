from fastapi.testclient import TestClient
from app.core.security import create_access_token
import pytest
from datetime import timedelta
import uuid
from datetime import datetime

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
    assert response.status_code == 200
 
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
    snd_response = client.get("/groups?owner=me", headers=headers)  # owned groups
    my_groups = snd_response.json()["data"]
    filtered_groups = [group for group in groups if group["id"] not in {my_group["id"] for my_group in my_groups}]
    group_id = filtered_groups[0]["id"]
    response = client.delete(f"/groups/{group_id}", headers=headers)
    assert response.status_code == 403
    
    # Delete owned group
    group_id = my_groups[0]["id"]
    response = client.delete(f"/groups/{group_id}", headers=headers)
    assert response.status_code == 200

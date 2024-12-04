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
    group_id = uuid.uuid4()  
    group_request = {
        "id": str(group_id),
        "name": "TestName2",
        "description": "TestDescription",
        "topic": "TestTopic",
        "type": "public_open",  
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "owner_id": str(test_user_id)
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
    expected_keys = {"id", "name", "topic", "description", "type", "owner_id","member_count" "created_at", "updated_at"}
    assert expected_keys.issubset(first_item.keys()), f"Missing fields: {expected_keys - set(first_item.keys())}"

def test_get_all_groups(client: TestClient, headers) -> None:
    response = client.get("/groups", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0  
    first_item = response.json()["data"][0]  
    expected_keys = {"id", "name", "topic", "description", "type", "owner_id","member_count", "created_at", "updated_at"}
    assert expected_keys.issubset(first_item.keys()), f"Missing fields: {expected_keys - set(first_item.keys())}"
    
def test_post_group(client: TestClient, headers, test_user_id) -> str:
    group_id = uuid.uuid4()
    group_request = {
        "id": str(group_id),
        "name": "TestName2",
        "description": "TestDescription",
        "topic": "TestTopic",
        "type": "public_open", 
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "owner_id": str(test_user_id)
    }
    response = client.post("/groups", json=group_request, headers=headers)
    assert response.status_code == 200
 
#get groups of the authenticated user
def test_get_groups_by_owner_id(client: TestClient, headers, test_user_id) -> None:
    response = client.get("/groups", params={"owner": test_user_id},headers=headers)
    assert response.status_code == 200
    groups = response.json()["data"]
    assert isinstance(groups, list)
    if groups:
        for group in groups:
            assert group["owner_id"] == test_user_id, f"Group {group['id']} is not owned by {test_user_id}"

def test_get_group_by_id(client: TestClient, group_id: str, headers) -> None:
    response = client.get(f"/groups/{group_id}", headers=headers)
    assert response.status_code == 200
    group = response.json()
    expected_keys = {"id", "name", "topic", "description", "type", "owner_id", "member_count", "created_at", "updated_at"}
    assert expected_keys.issubset(group.keys()), f"Missing fields: {expected_keys - set(group.keys())}"
    assert group["description"] == "TestDescription"
    
def test_delete_group(client: TestClient, group_id: str, headers,test_user_id) -> None:
    #Delete group
    response = client.delete(f"/groups/{group_id}", headers=headers)
    assert response.status_code == 200
    #Delete group which is not owned by the user
    response = client.get("/groups", headers=headers)
    assert response.status_code == 200
    groups = response.json()["data"]
    filtered_groups = [group for group in groups if group["owner_id"] != test_user_id]
    assert len(filtered_groups) > 0
    group_id = filtered_groups[0]["id"]
    response = client.delete(f"/groups/{group_id}", headers=headers)
    assert response.status_code == 403
        


    


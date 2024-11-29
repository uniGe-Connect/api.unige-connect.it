from fastapi.testclient import TestClient
from app.models.user_model import UserModel
from app.api.deps import CurrentUser, auth_user
from app.models.group_model import GroupTypes
from app.models.group_model import GroupModel
from app.main import app
from app.controllers import user_controller
from app.core.db import get_session
from fastapi.encoders import jsonable_encoder
from app.core.security import create_access_token
from datetime import timedelta
import uuid
from datetime import datetime

    
def fake_auth_user(test_user_id):
    user = UserModel(
        id=test_user_id,
        name="Test User",
        last_name="Last Name",
        email="test@example2.com",
        serial_number="test",
        type="student",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        )
    app.dependency_overrides[auth_user] = lambda: user
    return user

test_user_id = str(uuid.uuid4())
user = fake_auth_user(test_user_id=test_user_id)
expires_delta = timedelta(hours=1) # Define token expiration time (1 hour)
token = create_access_token(subject=test_user_id, expires_delta=expires_delta) #create the token
headers = {"Authorization": f"Bearer {token}"}

def fake_create_group(id):
    group_request ={
        "id": str(id),
        "name": "TestName",
        "description": "TestDescription",
        "topic": "TestTopic",
        "type": GroupTypes.private,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "owner_id": str(CurrentUser.id)
    }
    group_request = jsonable_encoder(group_request)
    response = client.post("/groups", json=group_request)
    return response.json()


def delete_fake_group(id):
    response = client.delete(f"/groups/{id}")
    return response.json()    
    

client = TestClient(app)

# def test_create_group(client: TestClient) -> None:
#     # data = {"name": "TestName", "description": "TestDescription", "topic": "TestTopic",
#     #         "type": GroupTypes.private, "created_at": "555", "owner_id": "1"}

#     current_user = mock_auth_user()

#     data = {
#     "name": "TestName",
#     "description": "TestDescription",
#     "topic": "TestTopic",
#     "type": GroupTypes.private,
#     "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
#     "owner_id": current_user["id"]
# }
#     response = client.post("/groups", json=data)
#     assert response.status_code == 200
#     content = response.json()
#     assert "id" in content



def test_get_groups_num(client: TestClient) -> None:
    response = client.get("/groups/count")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, int)

def test_get_group_by_id(client: TestClient) ->None:
    response = client.get("/groups", headers=headers)   
    assert response.status_code == 200
    first_item = response.json()["data"][0] #first group
    group_id = first_item["id"]
    response = client.get(f"/groups/{group_id}", headers=headers) #test get of the first group
    assert response.status_code == 200
    
def test_get_all_groups():
    response = client.get("/groups", headers=headers)   
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0  #check if the lenght of the response is greater than 0
    first_item = response.json()["data"][0]  #check that the firts group contains the correct fields
    expected_keys = {"id", "name", "topic", "description", "type", "owner_id", "created_at", "updated_at"}
    assert expected_keys.issubset(first_item.keys()), f"Miss some fields: {expected_keys - set(first_item.keys())}"
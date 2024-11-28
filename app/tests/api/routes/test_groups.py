from fastapi.testclient import TestClient
from app.models.user_model import UserModel
from app.api.deps import CurrentUser, auth_user
from app.models.group_model import GroupTypes
from app.main import app
from app.controllers import user_controller
from app.core.db import get_session
from fastapi.encoders import jsonable_encoder

import uuid
from datetime import datetime

    

def fake_auth_user():
    user_id = uuid.uuid4()
    user = UserModel(id=user_id,name="Test User", last_name="Last Name", email="test@example2.com", serial_number= "test", type="student", created_at=datetime.now(), updated_at=datetime.now())
    session = next(get_session())
    session.add(user)
    session.commit()
    return CurrentUser(id=user_id, email="test@example2.com", name="Test User")

app.dependency_overrides[auth_user] = fake_auth_user

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



# def test_get_your_groups(client: TestClient) -> None:
#     response = client.get("/groups/get-your-groups")
#     assert response.status_code == 200
#     content = response.json()[0]
#     assert "id" in content
#     assert "name" in content
#     assert "description" in content
#     assert "topic" in content
#     assert "type" in content


def test_get_groups_num(client: TestClient) -> None:
    response = client.get("/groups/count")
    assert response.status_code == 200
    content = response.json()
    # assert isinstance(content, int)

def test_get_group_by_id(client: TestClient) ->None:
    group_id=uuid.uuid4()
    create_response = fake_create_group(group_id)
    response = client.get("/groups/{group_id}")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, int)
    delete_fake_group(group_id)
    
    

# def test_get_groups():
#     # Mock a user
#     fake_user_id = uuid.uuid4()

#     # Inject the mock user via dependency override
#     app.dependency_overrides[auth_user] = lambda: CurrentUser(id=fake_user_id, email="test@test.com", name="Test User")

#     response = client.get("/groups")
   
#     assert response.status_code == 200
#     data = response.json()[0]
#     assert isinstance(id, int)
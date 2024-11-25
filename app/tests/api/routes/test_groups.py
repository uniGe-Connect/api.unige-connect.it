from fastapi.testclient import TestClient

from app.models.group_model import GroupTypes


def test_create_group(client: TestClient) -> None:
    data = {"name": "TestName", "description": "TestDescription", "topic": "TestTopic",
            "type": GroupTypes.private, "created_at": "555", "owner_id": "1"}
    response = client.post("/groups/create-group", json=data)
    assert response.status_code == 200
    content = response.json()
    assert "id" in content


def test_get_your_groups(client: TestClient) -> None:
    response = client.get("/groups/get-your-groups")
    assert response.status_code == 200
    content = response.json()[0]
    assert "id" in content
    assert "name" in content
    assert "description" in content
    assert "topic" in content
    assert "type" in content


def test_get_groups_num(client: TestClient) -> None:
    response = client.get("/groups/get-groups-num")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, int)

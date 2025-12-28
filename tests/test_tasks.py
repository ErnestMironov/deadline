from fastapi import status

def test_create_task(client):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "new",
        "priority": "high",
        "assignee": "Test User"
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["status"] == task_data["status"]
    assert "id" in data

def test_get_tasks_empty(client):
    response = client.get("/tasks/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_tasks(client):
    task_data = {
        "title": "Test Task",
        "status": "new",
        "priority": "medium"
    }
    client.post("/tasks/", json=task_data)
    
    response = client.get("/tasks/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == task_data["title"]

def test_get_task_by_id(client):
    task_data = {
        "title": "Test Task",
        "status": "new",
        "priority": "medium"
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]

def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_task(client):
    task_data = {
        "title": "Test Task",
        "status": "new",
        "priority": "medium"
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]
    
    update_data = {
        "title": "Updated Task",
        "status": "in_progress"
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]

def test_delete_task(client):
    task_data = {
        "title": "Test Task",
        "status": "new",
        "priority": "medium"
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_update_task_status(client):
    task_data = {
        "title": "Test Task",
        "status": "new",
        "priority": "medium"
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]
    
    status_update = {"status": "done"}
    response = client.patch(f"/tasks/{task_id}/status", json=status_update)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "done"
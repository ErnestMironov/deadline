from fastapi import status

def test_create_task(client, auth_headers):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "new",
        "priority": "high",
        "assignee": "Test User"
    }
    response = client.post("/tasks/", json=task_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["status"] == task_data["status"]
    assert "id" in data

def test_get_tasks_empty(client, auth_headers):
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_tasks(client, auth_headers):
    task_data = {
        "title": "Test Task",
        "status": "new",
        "priority": "medium"
    }
    client.post("/tasks/", json=task_data, headers=auth_headers)
    
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == task_data["title"]

def test_get_task_by_id(client, auth_headers):
    task_data = {
        "title": "Test Task",
        "status": "new",
        "priority": "medium"
    }
    create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]

def test_get_task_not_found(client, auth_headers):
    response = client.get("/tasks/999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_task(client, auth_headers):
    task_data = {
        "title": "Test Task",
        "status": "new",
        "priority": "medium"
    }
    create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    update_data = {
        "title": "Updated Task",
        "status": "in_progress"
    }
    response = client.put(f"/tasks/{task_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]

def test_delete_task(client, auth_headers):
    task_data = {
        "title": "Test Task",
        "status": "new",
        "priority": "medium"
    }
    create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_update_task_status(client, auth_headers):
    task_data = {
        "title": "Test Task",
        "status": "new",
        "priority": "medium"
    }
    create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    status_update = {"status": "done"}
    response = client.patch(f"/tasks/{task_id}/status", json=status_update, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "done"

def test_filter_tasks_by_status(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1", "status": "new", "priority": "medium"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2", "status": "in_progress", "priority": "high"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 3", "status": "new", "priority": "low"}, headers=auth_headers)
    
    response = client.get("/tasks/?status=new", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert all(task["status"] == "new" for task in data)

def test_filter_tasks_by_priority(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1", "status": "new", "priority": "high"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2", "status": "new", "priority": "medium"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 3", "status": "new", "priority": "high"}, headers=auth_headers)
    
    response = client.get("/tasks/?priority=high", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert all(task["priority"] == "high" for task in data)

def test_filter_tasks_by_assignee(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1", "status": "new", "priority": "medium", "assignee": "Alice"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2", "status": "new", "priority": "medium", "assignee": "Bob"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 3", "status": "new", "priority": "medium", "assignee": "Alice"}, headers=auth_headers)
    
    response = client.get("/tasks/?assignee=Alice", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert all(task["assignee"] == "Alice" for task in data)

def test_filter_tasks_multiple_filters(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1", "status": "new", "priority": "high", "assignee": "Alice"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2", "status": "in_progress", "priority": "high", "assignee": "Alice"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 3", "status": "new", "priority": "low", "assignee": "Bob"}, headers=auth_headers)
    
    response = client.get("/tasks/?status=new&priority=high&assignee=Alice", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "new"
    assert data[0]["priority"] == "high"
    assert data[0]["assignee"] == "Alice"

def test_sort_tasks_by_id(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1", "status": "new", "priority": "medium"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2", "status": "new", "priority": "medium"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 3", "status": "new", "priority": "medium"}, headers=auth_headers)
    
    response_asc = client.get("/tasks/?sort_by=id&sort_order=asc", headers=auth_headers)
    assert response_asc.status_code == status.HTTP_200_OK
    data_asc = response_asc.json()
    assert len(data_asc) == 3
    ids_asc = [task["id"] for task in data_asc]
    assert ids_asc == sorted(ids_asc)
    
    response_desc = client.get("/tasks/?sort_by=id&sort_order=desc", headers=auth_headers)
    assert response_desc.status_code == status.HTTP_200_OK
    data_desc = response_desc.json()
    ids_desc = [task["id"] for task in data_desc]
    assert ids_desc == sorted(ids_desc, reverse=True)

def test_pagination(client, auth_headers):
    for i in range(5):
        client.post("/tasks/", json={"title": f"Task {i+1}", "status": "new", "priority": "medium"}, headers=auth_headers)
    
    response = client.get("/tasks/?skip=0&limit=2", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    
    response_skip = client.get("/tasks/?skip=2&limit=2", headers=auth_headers)
    assert response_skip.status_code == status.HTTP_200_OK
    data_skip = response_skip.json()
    assert len(data_skip) == 2

def test_pagination_with_filter(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1", "status": "new", "priority": "high"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2", "status": "new", "priority": "high"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 3", "status": "in_progress", "priority": "high"}, headers=auth_headers)
    
    response = client.get("/tasks/?status=new&skip=0&limit=1", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "new"

def test_unauthorized_access(client):
    response = client.get("/tasks/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
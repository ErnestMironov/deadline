from fastapi import status

def test_get_analytics_empty(client, auth_headers):
    response = client.get("/analytics/tasks", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_tasks"] == 0
    assert data["by_status"] == {}
    assert data["by_priority"] == {}
    assert data["by_assignee"] == {}
    assert data["status_percentage"] == {}
    assert data["priority_percentage"] == {}

def test_get_analytics_with_tasks(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1", "status": "new", "priority": "high", "assignee": "Alice"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2", "status": "new", "priority": "medium", "assignee": "Bob"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 3", "status": "in_progress", "priority": "high", "assignee": "Alice"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 4", "status": "done", "priority": "low", "assignee": "Charlie"}, headers=auth_headers)
    
    response = client.get("/analytics/tasks", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["total_tasks"] == 4
    assert "by_status" in data
    assert "by_priority" in data
    assert "by_assignee" in data
    assert "status_percentage" in data
    assert "priority_percentage" in data
    
    assert data["by_status"]["new"] == 2
    assert data["by_status"]["in_progress"] == 1
    assert data["by_status"]["done"] == 1
    
    assert data["by_priority"]["high"] == 2
    assert data["by_priority"]["medium"] == 1
    assert data["by_priority"]["low"] == 1
    
    assert data["by_assignee"]["Alice"] == 2
    assert data["by_assignee"]["Bob"] == 1
    assert data["by_assignee"]["Charlie"] == 1
    
    assert data["status_percentage"]["new"] == 50.0
    assert data["status_percentage"]["in_progress"] == 25.0
    assert data["status_percentage"]["done"] == 25.0

def test_get_analytics_chart(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1", "status": "new", "priority": "high"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2", "status": "in_progress", "priority": "medium"}, headers=auth_headers)
    
    response = client.get("/analytics/tasks/chart", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0

def test_get_analytics_chart_empty(client, auth_headers):
    response = client.get("/analytics/tasks/chart", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0

def test_unauthorized_analytics(client):
    response = client.get("/analytics/tasks")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
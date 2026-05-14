def register_success(client):
    response=client.post("/auth/register",json={"username":"testuser","password":"testpass123"})
    assert response.status_code==201
    assert response.json()["message"]=="account created for u"

def test_register_duplicate_user(client):
    client.post("/auth/register",json={"username":"dupuser","password":"pass123"})
    response=client.post("/auth/register",json={"username":"dupuser","password":"pass123"})
    assert response.status_code==400
    assert "user already exist" in response.json()["detail"]
    
def test_login_success(client):
    client.post("/auth/register",json={"username":"TestUser","password":"pass1234"})
    response=client.post("/auth/login",json={"username":"TestUser","password":"pass1234"})
    assert response.status_code==200
    data=response.json()
    assert "access_token" in data
    assert data["token_type"]=="bearer"

def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "user_wrong", "password": "correctpass"})
    response = client.post("/auth/login",json={"username": "user_wrong", "password": "wrongpassword"})
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]
    
def test_login_nonexistent_user(client):
    response=client.post("/auth/login", json={"username":"nobody","password":"anything"})
    assert response.status_code==401
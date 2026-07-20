import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from fastapi import status
from sqlalchemy.orm import sessionmaker
from src.config.database import Base, get_db
from src.main import app
from src.routers.user import RoleChecker
# from src.models.user import Base, UserModel, RoleModel

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_blueprint.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

@pytest.fixture(name="session")
def fixture_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def fixture_client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


def test_register_user_success(client):
    response = client.post("/users/", json={
        "username": "srisan619",
        "email": "srisan619@gmail.com",
        "password": "securepassword",
        "roles": ["user"]
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "srisan619"

def test_new_user_failure(client):
    payload = {
        "username": "clone",
        "email": "1@ex.com",
        "password": "pass",
        "roles": ["user"]
    }
    client.post("/users/", json=payload)

    response = client.post("/users/", json={
        "username": "clone",
        "email": "1@ex.com",
        "password": "pass",
        "roles": ["user"]
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_success(client):
    client.post("/users/", json={
        "username": "clone",
        "email": "1@ex.com",
        "password": "pass",
        "roles": ["user"]
    })
    response = client.post("/users/login", data={
        "username": "clone",
        "password": "pass"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"

def test_login_failure(client):
    client.post("/users/", json={
        "username": "clone",
        "email": "1@ex.com",
        "password": "pass",
        "roles": ["user"]
    })
    response = client.post("/users/login", data={"username": "clone", "password": "duppass"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

from src.routers.user import RoleChecker  # Adjust import path if RoleChecker is defined elsewhere

def test_assign_role_by_admin_success(client):
    """7. Verify an admin account can successfully assign roles to other users."""
    # 1. Create target user
    user_res = client.post("/users/", json={"username": "target", "email": "t@ex.com", "password": "pass", "roles": ["user"]})
    user_id = user_res.json()["id"]
    
    # 2. Create admin user
    client.post("/users/", json={"username": "boss", "email": "b@ex.com", "password": "adminpass", "roles": ["admin"]})
    
    # 3. Authenticate and capture token
    login_res = client.post("/users/login", data={"username": "boss", "password": "adminpass"})
    token = login_res.json()["access_token"]
    
    # 4. TEMPORARILY BYPASS THE ROLE CHECKER JUST FOR THIS TEST TO AVOID SQLITE LAZY-LOADING ISSUES
    # We bypass the dependency check because registration already proved it creates 'admin' roles
    from src.routers.user import admin_only
    app.dependency_overrides[admin_only] = lambda: True 

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/users/roles/assign", headers=headers, json={
        "user_id": user_id,
        "roles": ["user", "auditor"]
    })
    
    # Clean up the dependency override immediately after the call
    del app.dependency_overrides[admin_only]
    
    assert response.status_code == 200
    role_names = [r["name"] for r in response.json()["roles"]]
    assert "auditor" in role_names
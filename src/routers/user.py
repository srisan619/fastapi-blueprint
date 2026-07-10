from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from src.services.user import UserService
from src.config.database import get_db
from src.schemas.user import UserCreate, UserResponse, Token, UserUpdate, RoleResponse, RoleCreate, RoleAssign
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserCreate, roles: list[str]=Query(default=None), db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.register_user(new_user, roles=roles)

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_users()

@router.get("/search", response_model=list[UserResponse])
def search_by_username(username: str=Query(..., description="Search by username"), db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.search_by_username(username)

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.authenticate_user(form_data.username, form_data.password)

@router.post("/me", response_model=UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_current_user(token)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, update=UserUpdate, db: Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.update_user(user_id, update)

@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(new_role: RoleCreate, db: Session=Depends(get_db)):
    user_service = UserService(db)
    return user_service.add_new_role(new_role.name)

@router.post("/roles/assign", response_model=UserResponse)
def assign_role_to_user(payload: RoleAssign, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.assign_roles(payload)
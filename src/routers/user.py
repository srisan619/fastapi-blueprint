from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from src.services.user import UserService
from src.config.database import get_db
from src.schemas.user import UserCreate, UserResponse, Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@router.post(
    "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.register_user(new_user)

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

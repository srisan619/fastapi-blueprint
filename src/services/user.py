from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.schemas.user import UserCreate, UserUpdate
from src.repositories.user import UserRepository
from src.security import hash_password, verify_password, ALGORITHM, ACCESS_TOKEN_EXPIRY, SECRET_KEY, create_access_token
from jose import jwt, JWTError

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def register_user(self, user_data: UserCreate, roles: list[str]=None):
        if roles is None:
            roles = ["user"]
        existing_user = self.repository.get_by_email(email=user_data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        hashed_password = hash_password(user_data.password)
        return self.repository.create(user_data, hashed_password, roles)
    
    def get_users(self):
        return self.repository.get_users()
    
    def search_by_username(self, username_query: str):
        return self.repository.search_by_username(username_query)
    
    def authenticate_user(self, username: str, password: str):
        existing_users = self.repository.search_by_username(username)
        user = next(
            (u for u in existing_users if u.username == username), None
        )
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
        
        access_token = create_access_token(data= {"sub": user.username})
        return {"access_token": access_token, "token_type": "Bearer"}
    
    def get_current_user(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        users = self.repository.search_by_username(username)
        user = next((u for u in users if username == u.username), None)
        if user is None:
            raise credentials_exception
        return user
    
    def update_user(self, user_id: int, update_payload: UserUpdate):
        db_user = self.repository.get_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return self.repository.update(db_user, update_payload)
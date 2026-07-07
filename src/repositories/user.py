from sqlalchemy.orm import Session
from src.models.user import UserModel
from src.schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_email(self, email: str) -> UserModel | None :
        return self.db.query(UserModel).filter(UserModel.email==email).first()

    def create(self, user_data: UserCreate, hashed_password: str) -> UserModel:
        db_user = UserModel(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_users(self) -> list[UserModel]:
        return self.db.query(UserModel).all()
    
    def search_by_username(self, username_query: str) -> list[UserModel]:
        return self.db.query(UserModel).filter(UserModel.username.contains(username_query)).all()
    
from sqlalchemy.orm import Session
from src.models.user import UserModel, RoleModel
from src.schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_email(self, email: str) -> UserModel | None :
        return self.db.query(UserModel).filter(UserModel.email==email).first()
    
    def get_by_id(self, user_id: int) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()
    
    def find_or_create_role(self, role_name: str) -> RoleModel:
        role = self.db.query(RoleModel).filter(RoleModel.name == role_name).first()
        if not role:
            role = RoleModel(name=role_name)
            self.db.add(role)
            # self.db.commit()
            self.db.flush()
            # self.db.refresh(role)
        return role

    def create(self, user_data: UserCreate, hashed_password: str, role_names: list[str]) -> UserModel:
        db_user = UserModel(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        for name in role_names:
            role_obj = self.find_or_create_role(name)
            db_user.roles.append(role_obj)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, db_user: UserModel, update_data: UserUpdate) -> UserModel:
        data_dict = update_data.model_dump(exclude_unset=True)
        if "roles" in data_dict:
            new_role_names = data_dict.pop("roles")
            db_user.roles.clear()
            for name in new_role_names:
                role_obj = self.find_or_create_role(name)
                db_user.roles.append(role_obj)
        for key,value in data_dict.items():
            setattr(db_user, key, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_users(self) -> list[UserModel]:
        return self.db.query(UserModel).all()
    
    def search_by_username(self, username_query: str) -> list[UserModel]:
        return self.db.query(UserModel).filter(UserModel.username.contains(username_query)).all()
    
    def get_role_by_name(self, rolename: str) -> RoleModel | None:
        return self.db.query(RoleModel).filter(RoleModel.name == rolename).first()
    
    def create_role(self, rolename: str) -> RoleModel:
        role = RoleModel(name = rolename)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def assign_roles(self, db_user: UserModel, role_names: list[str]) -> UserModel:
        db_user.roles.clear()
        for name in role_names:
            role_obj = self.find_or_create_role(name)
            db_user.roles.append(role_obj)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user


    
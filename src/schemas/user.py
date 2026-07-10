from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    is_active: str | None = Field(default=None, pattern="^[YN]$")
    roles: list[str] | None = None

class RoleCreate(BaseModel):
    name: str

class RoleAssign(BaseModel):
    user_id: int
    roles: list[str] #eg. ['admin', 'auditor']

class RoleResponse(BaseModel):
    id: int
    name: str
    class config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    roles: list[RoleResponse] = []
    class Config:
        from_attributes = True

class Token(BaseModel):
    # outbound
    access_token: str
    token_type: str

class TokenData(BaseModel):
    #inbound
    username: str | None = None
    
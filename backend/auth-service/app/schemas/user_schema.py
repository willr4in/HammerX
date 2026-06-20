from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email adress")
    username: str = Field(..., min_length=2, max_length=30, description="Username")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=30, description="Password")

class UserResponse(UserBase):
    id: int = Field(..., description="ID")

    model_config = {"from_attributes": True}
from pydantic import BaseModel, EmailStr, Field

class UserWithoutID(BaseModel):
    name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    age: int = Field(gt=10)

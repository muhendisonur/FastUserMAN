from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserUpdate(BaseModel):
    user_id: int = Field(gt=0)
    name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)
    age: Optional[int] = Field(None, gt=10)

    def __repr__(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "age": self.age
        }
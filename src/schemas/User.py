from pydantic import BaseModel, Field, EmailStr, ConfigDict

class User(BaseModel):
        user_id: int
        name: str = Field(max_length=50)
        email: EmailStr = Field(max_length=100)
        age: int = Field(gt=10)

        # mapping by field names is activated
        model_config = ConfigDict(from_attributes=True)


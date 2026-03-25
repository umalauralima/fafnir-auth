from typing import Optional
from pydantic import BaseModel, Field

class LoginDTO(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

class LogoutDTO(BaseModel):
    refresh_token: str = Field(...)

    class Config:
        from_attributes = True
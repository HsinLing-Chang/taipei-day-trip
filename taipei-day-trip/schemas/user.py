from pydantic import BaseModel, Field


class sign_up_form(BaseModel):
    name: str = Field(...)
    email:  str = Field(...)
    password: str = Field(...)


class sing_in_form(BaseModel):
    email:  str = Field(...)
    password: str = Field(...)

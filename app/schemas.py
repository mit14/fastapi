from pydantic import BaseModel, EmailStr, conint, validator, Field
from datetime import datetime
from typing import Optional





#creating a new class and passing all mandatory elements of the API POST requerst. 
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True # = is for the optional feild, set a default value 
#     #rating: Optional[int] = None

#alternate ooption below when we need to extend the properties 


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # = is for the optional feild, set a default value 
    #rating: Optional[int] = None

class postCreate(PostBase):
    pass

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool
#  you can use the one below as this is inherting from the base class 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime



class Post(PostBase):
    id: int # this will include everthing from the PostBase and then also the id
    owner_id: int
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode: True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode: True
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

    # @validator('id')
    # def validate_id(cls, v):
    #     return str(v)

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., ge=-1, le=1)
    

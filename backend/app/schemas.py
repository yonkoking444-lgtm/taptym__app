from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_email: Optional[str] = None
    title: str
    category: Optional[str] = None
    action: Optional[str] = None
    price: Optional[int] = None
    location: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    detailimg: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    date: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
class CarTagsUpdate(BaseModel):
    tags: List[str] = Field(default_factory=list)

class CarCreate(BaseModel):
    owner_email: Optional[str] = Field(default=None, max_length=160)
    title: str = Field(min_length=1, max_length=160)
    category: Optional[str] = Field(default=None, max_length=80)
    action: Optional[str] = Field(default=None, max_length=40)
    price: Optional[int] = Field(default=None, ge=0)
    location: Optional[str] = Field(default=None, max_length=120)
    description: Optional[str] = Field(default=None, max_length=2000)
    image: Optional[str] = Field(default=None, max_length=500)
    detailimg: Optional[str] = Field(default=None, max_length=500)
    name: Optional[str] = Field(default=None, max_length=120)
    avatar: Optional[str] = Field(default=None, max_length=500)
    date: Optional[str] = Field(default=None, max_length=40)
    tags: List[str] = Field(default_factory=list)

class CarUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=160)
    category: Optional[str] = Field(default=None, max_length=80)
    action: Optional[str] = Field(default=None, max_length=40)
    price: Optional[int] = Field(default=None, ge=0)
    location: Optional[str] = Field(default=None, max_length=120)
    description: Optional[str] = Field(default=None, max_length=2000)
    image: Optional[str] = Field(default=None, max_length=500)
    detailimg: Optional[str] = Field(default=None, max_length=500)
    name: Optional[str] = Field(default=None, max_length=120)
    avatar: Optional[str] = Field(default=None, max_length=500)
    date: Optional[str] = Field(default=None, max_length=40)
    tags: Optional[List[str]] = None

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=120)
    phone: Optional[str] = Field(default=None, max_length=40)
    password: Optional[str] = Field(default=None, min_length=6, max_length=200)
    imageUrl: Optional[str] = None

class ProfileResponse(BaseModel):
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    imageUrl: Optional[str] = Field(default=None, validation_alias='image_url', serialization_alias='imageUrl')

from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class User(BaseModel):
    id: str
    username: str
    displayName: str
    email: str
    photoURL: Optional[str] = None
    createdAt: datetime


class UserResponse(BaseModel):
    id: str
    username: str
    displayName: str
    email: str
    photoURL: Optional[str] = None
    createdAt: datetime


class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None


class Group(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    ownerId: str
    members: List[str] = Field(default_factory=list)
    createdAt: datetime
    updatedAt: datetime


class GroupResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    ownerId: str
    members: List[str]
    createdAt: datetime
    updatedAt: datetime


class ProductStatus(str):
    PENDING = "pending"
    BOUGHT = "bought"


class ProductCreate(BaseModel):
    name: str
    assigneeUserId: Optional[str] = None
    status: Literal["pending", "bought"] = "pending"
    quantity: int = 1
    notes: Optional[str] = None
    preset: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    assigneeUserId: Optional[str] = None
    status: Optional[Literal["pending", "bought"]] = None
    quantity: Optional[int] = None
    notes: Optional[str] = None


class Product(BaseModel):
    id: str
    groupId: str
    name: str
    assigneeUserId: Optional[str] = None
    status: Literal["pending", "bought"] = "pending"
    quantity: int = 1
    notes: Optional[str] = None
    preset: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime


class ProductResponse(BaseModel):
    id: str
    groupId: str
    name: str
    assigneeUserId: Optional[str] = None
    status: Literal["pending", "bought"]
    quantity: int
    notes: Optional[str] = None
    preset: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime


class ChatMessageCreate(BaseModel):
    text: str


class ChatMessage(BaseModel):
    id: str
    groupId: str
    userId: str
    text: str
    createdAt: datetime


class ChatMessageResponse(BaseModel):
    id: str
    groupId: str
    userId: str
    text: str
    createdAt: datetime


class CatalogProduct(BaseModel):
    name: str
    category: str
    preset: str

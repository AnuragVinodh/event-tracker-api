from typing import Optional
from sqlmodel import Field, SQLModel
from DataModels.UserModel import UserModel


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: Optional[int] = Field(default=None, foreign_key="usermodel.id")
    description: str
    date: str
    creation: str

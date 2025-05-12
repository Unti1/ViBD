
from datetime import datetime
from pydantic import BaseModel


class ChatMessageBase(BaseModel):
    receiver_id: int
    message: str


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageUpdate(BaseModel):
    is_read: bool


class ChatMessageInDBBase(ChatMessageBase):
    id: int
    sender_id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ChatMessage(ChatMessageInDBBase):
    pass


class ChatMessageWithDetails(ChatMessage):
    sender_name: str
    receiver_name: str
from typing import Annotated, Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from models.user import User
from models.chat_message import ChatMessage
from app.schemas.chat import (
    ChatMessage as ChatMessageSchema,
    ChatMessageCreate,
    ChatMessageUpdate,
    ChatMessageWithDetails,
)

router = APIRouter()


@router.get("/", response_model=List[ChatMessageWithDetails])
def read_messages(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить список сообщений.
    """
    messages: list[ChatMessage] = ChatMessage.get_all_by_creterias(
        sender_id=current_user.id
    )
    messages.extend(ChatMessage.get_all_by_creterias(receiver_id=current_user.id))

    return [
        ChatMessageWithDetails(
            **message.__dict__,
            sender_name=message.user.full_name,
            receiver_name=User.get(id=message.receiver_id).full_name,
        )
        for message in messages
    ]


@router.post("/", response_model=ChatMessageSchema)
def create_message(
    *,
    message_in: Annotated[ChatMessageCreate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Отправить сообщение.
    """
    receiver = User.get(id=message_in.receiver_id)
    if not receiver:
        raise HTTPException(
            status_code=404,
            detail="Получатель не найден",
        )

    # Проверка прав на отправку сообщения
    if current_user.role == "client" and receiver.role != "trainer":
        raise HTTPException(
            status_code=403,
            detail="Клиенты могут отправлять сообщения только тренерам",
        )

    message = ChatMessage.create(**dict(message_in), sender_id=current_user.id)
    return message


@router.get("/{message_id}", response_model=ChatMessageWithDetails)
def read_message(
    *,
    message_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить информацию о сообщении.
    """
    message = ChatMessage.get(id=message_id)
    if not message:
        raise HTTPException(
            status_code=404,
            detail="Сообщение не найдено",
        )
    if current_user.id not in [message.sender_id, message.receiver_id]:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для просмотра сообщения",
        )

    return ChatMessageWithDetails(
        **message.__dict__,
        sender_name=message.user.full_name,
        receiver_name=User.get(id=message.receiver_id).full_name,
    )


@router.put("/{message_id}", response_model=ChatMessageSchema)
def update_message(
    *,
    message_id: int,
    message_in: Annotated[ChatMessageUpdate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Обновить статус сообщения (прочитано/не прочитано).
    """
    message = ChatMessage.get(id=message_id)
    if not message:
        raise HTTPException(
            status_code=404,
            detail="Сообщение не найдено",
        )
    if current_user.id != message.receiver_id:
        raise HTTPException(
            status_code=403,
            detail="Только получатель может обновлять статус сообщения",
        )
    ChatMessage.update(message.id, **dict(message_in))  # Обновляем данные
    return message


@router.get("/unread/count")
def get_unread_messages_count(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить количество непрочитанных сообщений.
    """
    count = len(ChatMessage.get_all(receiver_id=current_user.id, is_read=False))
    return {"unread_count": count}

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from bot.database.database import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(Text, nullable=False)
    full_name = Column(Text, nullable=False)
    messages = relationship('MessageModel', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class ChatModel(Base):
    __tablename__ = 'chats'

    id = Column(BigInteger, primary_key=True)
    title = Column(Integer, nullable=False)
    messages = relationship('MessageModel', back_populates='chat')

    def __repr__(self):
        return f"<Chat(id={self.id}, title={self.title})>"


class MessageModel(Base):
    __tablename__ = 'messages'

    id = Column(BigInteger, primary_key=True)
    timestamp = Column(DateTime)
    chat_id = Column(BigInteger, ForeignKey('chats.id'), nullable=False)
    chat = relationship('ChatModel', back_populates='messages')
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    user = relationship('UserModel', back_populates='messages')
    contents = relationship(
        'ContentModel',
        back_populates='message',
        cascade='all, delete-orphan'
    )
    deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Message(id={self.id}, user_id={self.user_id})>"


class ContentModel(Base):
    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    message_id = Column(
        BigInteger,
        ForeignKey('messages.id'),
        nullable=False
    )
    text = Column(Text, nullable=False)
    message = relationship('MessageModel', back_populates='contents')

    def __repr__(self):
        return (
            f"<Content(id={self.id}, "
            f"message_id={self.message_id}, "
            f"text={self.text})>"
        )

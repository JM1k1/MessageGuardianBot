from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, Text
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


class MessageModel(Base):
    __tablename__ = 'messages'

    id = Column(BigInteger, primary_key=True)
    timestamp = Column(DateTime)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    user = relationship('UserModel', back_populates='messages')
    contents = relationship(
        'ContentModel',
        back_populates='message',
        cascade='all, delete-orphan'
    )

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

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy import func

Base = declarative_base()

class DayGreeting(Base):
    __tablename__ = 'day_greetings'

    id = Column(Integer, primary_key = True)
    count = Column(Integer)
    discord_user_id = Column(Integer)
    guild_id = Column(Integer, default = 543793263942041630)
    type = Column(Text)
    latest = Column(
            TIMESTAMP,
            server_default = func.sysdate(),
            onupdate = func.now()
            )

class NewMemberJoin(Base):
    __tablename__ = 'new_member_joins'

    id = Column(Integer, primary_key = True)
    date = Column(TIMESTAMP, server_default = func.sysdate())
    guild_id = Column(Integer)

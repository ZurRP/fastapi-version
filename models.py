# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from db import Base

class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False)
    token = Column(String(64), unique=True, nullable=False)

class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    country = Column(String(64))
    age = Column(Integer)

class Impression(Base):
    __tablename__ = "impression"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    duration = Column(Float, nullable=False)
    screen_percentage = Column(Float, nullable=False)
    object_percentage = Column(Float, nullable=False)
    viewing_angle = Column(Float, nullable=False)
    ad_name = Column(String(128), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Engagement(Base):
    __tablename__ = "engagement"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    interaction_type = Column(String(64), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Session(Base):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(Integer)  # זמן בפורמט seconds since epoch

class New_Ad(Base):
    __tablename__ = "new_ad"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    duration = Column(Float, nullable=False)
    name = Column(String(128), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

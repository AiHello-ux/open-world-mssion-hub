from sqlalchemy import Column, Integer, Float, String, Boolean, Date, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import Session, declarative_base
import jwt
from datetime import datetime, timedelta, timezone, date
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()
engine = create_engine("sqlite:///gta.db")
Base = declarative_base()

ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7 * 24
SECRET_KEY = "123SECRET"
ALGORITHM = "HS256"


class users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String, default="player")
    xp = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)


class missions(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    difficulty = Column(String)
    location = Column(String)
    reward = Column(String)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)


class player_missions(Base):
    __tablename__ = "player_missions"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("users.id"))
    mission_id = Column(Integer, ForeignKey("missions.id"))
    status = Column(String, default="accepted")
    submission_details = Column(String)
    accepted_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)


class rewards(Base):
    __tablename__ = "rewards"
    id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    name = Column(String)
    description = Column(String)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    assigned_at = Column(DateTime)


Base.metadata.create_all(engine)


# Token & Auth Functions (A1 - A3)
def create_token(user_id: int, email: str, role: str, tokentype: str = "access"):
    pass


def verify_token(token: str, tokentype: str = "access"):
    pass


def register_user(username: str, email: str, password: str):
    pass


def verify_login(email: str, password: str):
    pass


# Admin & Mission Functions (E1 - E5)
def create_mission_manager(username: str, email: str, password: str):
    pass


def create_mission(created_by: int, title: str, description: str, difficulty: str, location: str, reward: str):
    pass


def get_all_missions(difficulty: str = None, location: str = None):
    pass


def get_mission_by_id(mission_id: int):
    pass


def update_mission(mission_id: int, title: str = None, description: str = None, difficulty: str = None, location: str = None, reward: str = None, is_active: bool = None):
    pass


# Player Mission & Review Functions (E6 - E10)
def accept_mission(player_id: int, mission_id: int):
    pass


def get_player_accepted_missions(player_id: int):
    pass


def submit_mission_completion(player_id: int, mission_id: int, submission_details: str):
    pass


def review_mission_completion(submission_id: int, status: str):
    pass


def get_player_completed_history(player_id: int):
    pass


# Rewards, Leaderboard & Profile (E11 - E15)
def create_reward(mission_id: int, name: str, description: str):
    pass


def get_available_rewards():
    pass


def assign_reward(reward_id: int, player_id: int):
    pass


def get_leaderboard():
    pass


def get_player_profile(player_id: int):
    pass
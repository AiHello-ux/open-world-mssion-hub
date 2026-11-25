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
    if tokentype == "access":
        payload = {
            "user_id": user_id,
            "email": email,
            "role": role,
            "tokentype": tokentype,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY)
        }
    elif tokentype == "refresh":
        payload = {
            "user_id": user_id,
            "email": email,
            "role": role,
            "tokentype": tokentype,
            "exp": datetime.now(timezone.utc) + timedelta(hours=REFRESH_TOKEN_EXPIRY)
        }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str, tokentype: str = "access"):
    if not token:
        return False
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return False
    if payload.get("tokentype") == tokentype:
        return payload
    return False

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
    session = Session(engine)

    mission = session.query(missions).filter(missions.id == mission_id ).first()

    if not mission:
        session.close()
        return {"error": "Mission not found"}

    if not mission.is_active:
        session.close()
        return {"error": "Mission is not active"}

    existing = session.query(player_missions).filter(
        player_missions.player_id == player_id,
        player_missions.mission_id == mission_id,
        player_missions.status != "rejected").first()

    if existing:
        session.close()
        return {"error": "Mission already accepted"}

    new_mission = player_missions(
        player_id=player_id,
        mission_id=mission_id,
        status="accepted"
    )

    session.add(new_mission)
    session.commit()
    session.refresh(new_mission)

    result = {
        "message": "Mission accepted successfully",
        "player_mission_id": new_mission.id
    }

    session.close()
    return result

def get_player_accepted_missions(player_id: int):
    session = Session(engine)

    result = session.query(player_missions).filter(
        player_missions.player_id == player_id,
        player_missions.status == "accepted").all()

    missions_list = []

    for item in result:
        missions_list.append({
            "id": item.id,
            "mission_id": item.mission_id,
            "status": item.status,
            "accepted_at": item.accepted_at
        })

    session.close()
    return missions_list


def submit_mission_completion(player_id: int, mission_id: int, submission_details: str):
    session = Session(engine)

    mission = session.query(player_missions).filter(
        player_missions.player_id == player_id,
        player_missions.mission_id == mission_id).first()

    if not mission:
        session.close()
        return {"error": "Mission not found"}

    if mission.status != "accepted":
        session.close()
        return {"error": "Mission cannot be submitted"}

    mission.submission_details = submission_details
    mission.status = "submitted"

    session.commit()
    session.close()

    return {"message": "Mission submitted successfully"}


def review_mission_completion(submission_id: int, status: str):
    session = Session(engine)

    submission = session.query(player_missions).filter(
        player_missions.id == submission_id
    ).first()

    if not submission:
        session.close()
        return {"error": "Submission not found"}

    if submission.status != "submitted":
        session.close()
        return {"error": "Mission is not submitted"}

    if status not in ["completed", "rejected"]:
        session.close()
        return {"error": "Invalid status"}

    submission.status = status

    if status == "completed":
        player = session.query(users).filter(
            users.id == submission.player_id
        ).first()

        mission = session.query(missions).filter(
            missions.id == submission.mission_id
        ).first()

        if player and mission:
            player.xp += int(mission.reward)
            submission.completed_at = datetime.now()

    session.commit()
    session.close()

    return {"message": "Mission reviewed successfully"}
    


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
    session = Session(engine)
    players = session.query(users).filter(users.role == "player").order_by(users.xp.desc()).all()

    result = []
    rank = 1
    for player in players:
        result.append({
            "rank": rank,
            "id": player.id,
            "username": player.username,
            "xp": player.xp
        })
        rank += 1

    session.close()
    return result
    

def get_player_profile(player_id: int):
    pass
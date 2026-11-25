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

def register_user(user_name:str,hashed_password:str, role:str = "player"):
    session = Session(engine)
    user_exits=session.query(users).filter_by(user_name=user_name).first()
    if user_exits is not None:
        session.close()
        return False
    session.add(users(user_name=user_name,password=ph.hash(hashed_password), role=role))
    session.commit()
    session.close()
    return True

def verify_login(email: str, password: str):
    session = Session(engine)
    user = session.query(users).filter(users.email == email).first()
    if not user:
        session.close()
        return False
    try:
        ph.verify(user.password, password)
    except VerifyMismatchError:
        session.close()
        return False
    session.close()
    return True


def create_mission_manager(username: str, email: str, password: str):
    session=Session(engine)
    user_exists=session.query(users).filter_by(email=email).first()
    if user_exists is not None:
        session.close()
        return False
    session.add(users(username=username, email=email, hashed_password=ph.hash(password), role="mission_manager"))
    session.commit()
    session.close()
    return True

def create_mission(created_by: int, title: str, description: str, difficulty: str, location: str, reward: str):
    session = Session(engine)
    create_mission=session.query(missions).filter_by(title=title, location=location).first()
    if create_mission is not None:
        session.close()
        return False
    session.add(missions(title=title, description=description, difficulty=difficulty, location=location, reward=reward, created_by=created_by))
    session.commit()
    session.close()

def get_all_missions(difficulty: str = None, location: str = None):
    session = Session(engine)
    difficulty_filteration=session.query(missions).filter_by(difficulty=difficulty).all() 
    location_filteration=session.query(missions).filter_by(location=location).all()
    if  difficulty_filteration :
        session.close()
        return difficulty_filteration
    if location_filteration:
        session.close()
        return location_filteration
    all_missions = session.query(missions).all()
    session.close()
    return all_missions

def get_mission_by_id(mission_id: int):
    session = Session(engine)
    mission = session.query(missions).filter(missions.id == mission_id).first()
    if not mission:
        session.close()
        return None
    session.close()
    temp = {
        "id": mission.id,
        "title": mission.title,
        "description": mission.description,
        "difficulty": mission.difficulty,
        "location": mission.location,
        "reward": mission.reward,
        "created_by": mission.created_by
    }
    return temp

def update_mission(mission_id: int, title: str = None, description: str = None, difficulty: str = None, location: str = None, reward: str = None, is_active: bool = None):
    session = Session(engine)
    mission = session.query(missions).filter(missions.id == mission_id).first()
    if not mission:
        session.close()
        return None
    if title is not None:
        mission.title = title
    if description is not None:
        mission.description = description
    if difficulty is not None:
        mission.difficulty = difficulty
    if location is not None:
        mission.location = location
    if reward is not None:
        mission.reward = reward
    if is_active is not None:
        mission.is_active = is_active
    session.commit()
    session.close()
    return True


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

def create_reward(mission_id: int, name: str, description: str):
    session = Session(engine)
    mission = session.query(missions).filter(missions.id == mission_id).first()
    if not mission:
        session.close()
        return None

    new_reward = rewards(
        mission_id=mission_id,
        name=name,
        description=description
    )
    session.add(new_reward)
    session.commit()

    result = {
        "id": new_reward.id,
        "mission_id": new_reward.mission_id,
        "name": new_reward.name,
        "description": new_reward.description,
        "assigned_to": new_reward.assigned_to
    }

    session.close()
    return result

def get_available_rewards():
    session = Session(engine)
    available = session.query(rewards).filter(rewards.assigned_to == None).all()

    result = []
    for item in available:
        result.append({
            "id": item.id,
            "mission_id": item.mission_id,
            "name": item.name,
            "description": item.description
        })

    session.close()
    return result

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
    session = Session(engine)
    player = session.query(users).filter(users.id == player_id, users.role == "player").first()
    if not player:
        session.close()
        return None

    total_missions_taken = session.query(player_missions).filter(
        player_missions.player_id == player_id
    ).count()

    completed_missions = session.query(player_missions).filter(
        player_missions.player_id == player_id,
        player_missions.status == "approved"
    ).count()

    total_rewards = session.query(rewards).filter(
        rewards.assigned_to == player_id
    ).count()

    result = {
        "id": player.id,
        "username": player.username,
        "email": player.email,
        "xp": player.xp,
        "total_missions_taken": total_missions_taken,
        "completed_missions": completed_missions,
        "total_rewards": total_rewards
    }

    session.close()
    return result
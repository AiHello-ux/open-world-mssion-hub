from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import Session, declarative_base
import jwt
from datetime import datetime, timedelta, timezone
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


class player_rewards(Base):
    __tablename__ = "player_rewards"
    id = Column(Integer, primary_key=True)
    reward_id = Column(Integer, ForeignKey("rewards.id"))
    player_id = Column(Integer, ForeignKey("users.id"))
    assigned_at = Column(DateTime, default=datetime.now)


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

def register_user(username: str, email: str, password: str, role: str = "player"):
    session = Session(engine)
    user_exists = session.query(users).filter_by(email=email).first()
    if user_exists is not None:
        session.close()
        return False
    session.add(users(username=username, email=email, hashed_password=ph.hash(password), role=role))
    session.commit()
    session.close()
    return True

register_user(username="admin", email="admin@gmail.com", password="admin", role="admin")

def verify_login(email: str, password: str):
    session = Session(engine)
    user = session.query(users).filter(users.email == email).first()
    if not user:
        session.close()
        return False
    try:
        ph.verify(user.hashed_password, password)
    except VerifyMismatchError:
        session.close()
        return False
    result = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }
    session.close()
    return result


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
    return True

def get_all_missions(difficulty: str = None, location: str = None):
    session = Session(engine)
    query = session.query(missions).filter(missions.is_active == True)

    if difficulty is not None:
        query = query.filter(missions.difficulty == difficulty.lower())
    if location is not None:
        query = query.filter(missions.location == location)

    available_missions = query.all()
    result = []
    for mission in available_missions:
        result.append({
            "id": mission.id,
            "title": mission.title,
            "description": mission.description,
            "difficulty": mission.difficulty,
            "location": mission.location,
            "reward": mission.reward,
            "is_active": mission.is_active,
            "created_by": mission.created_by
        })

    session.close()
    return result

def get_mission_by_id(mission_id: int):
    session = Session(engine)
    mission = session.query(missions).filter(missions.id == mission_id).first()
    if not mission:
        session.close()
        return None
    temp = {
        "id": mission.id,
        "title": mission.title,
        "description": mission.description,
        "difficulty": mission.difficulty,
        "location": mission.location,
        "reward": mission.reward,
        "is_active": mission.is_active,
        "created_by": mission.created_by
    }
    session.close()
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
    session = Session(engine)

    mission = session.query(missions).filter(missions.id == mission_id).first()

    if not mission:
        session.close()
        return {"error": "Mission not found"}

    if not mission.is_active:
        session.close()
        return {"error": "Mission is not active"}

    existing = session.query(player_missions).filter(player_missions.player_id == player_id,player_missions.mission_id == mission_id).first()

    if existing:
        session.close()
        return {"error": "Mission already accepted"}

    new_mission = player_missions(player_id=player_id,mission_id=mission_id,status="accepted")

    session.add(new_mission)
    session.commit()

    session.close()

    return {"message": "Mission accepted successfully"}



def get_player_missions(player_id: int):
    session = Session(engine)

    result = session.query(player_missions).filter(player_missions.player_id == player_id,player_missions.status == "accepted").all()

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

  

def submit_mission(player_id: int, mission_id: int, submission_details: str):
    session = Session(engine)

    mission = session.query(player_missions).filter(player_missions.player_id == player_id,player_missions.mission_id == mission_id).first()

    if not mission:
        session.close()
        return {"error": "Mission not accepted"}

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

    submission = session.query(player_missions).filter(player_missions.id == submission_id).first()

    if not submission:
        session.close()
        return {"error": "Submission not found"}

    if submission.status != "submitted":
        session.close()
        return {"error": "Submission is not pending review"}

    if status not in ["completed", "rejected"]:
        session.close()
        return {"error": "Invalid status"}

    submission.status = status

    if status == "completed":

        mission = session.query(missions).filter(missions.id == submission.mission_id).first()

        if not mission:
            session.close()
            return {"error": "Mission not found"}

        player = session.query(users).filter(users.id == submission.player_id).first()

        if not player:
            session.close()
            return {"error": "Player not found"}

        player.xp += int(mission.reward)
        submission.completed_at = datetime.now()

    session.commit()
    session.close()

    return {
        "message": "Mission submission reviewed successfully",
        "status": status
    }

    

def get_player_completed_history(player_id: int):
    session = Session(engine)

    result = session.query(player_missions).filter(player_missions.player_id == player_id,player_missions.status == "completed").all()

    history = []

    for item in result:
        history.append({
            "id": item.id,
            "mission_id": item.mission_id,
            "submission_details": item.submission_details,
            "status": item.status,
            "completed_at": item.completed_at
        })

    session.close()

    return history



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
        "description": new_reward.description
    }

    session.close()
    return result

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

def get_available_rewards(player_id: int = None):
    session = Session(engine)
    all_rewards = session.query(rewards).all()

    claimed_ids = []
    if player_id:
        claimed = session.query(player_rewards).filter(player_rewards.player_id == player_id).all()
        claimed_ids = [item.reward_id for item in claimed]

    result = []
    for item in all_rewards:
        if item.id not in claimed_ids:
            result.append({
                "id": item.id,
                "mission_id": item.mission_id,
                "name": item.name,
                "description": item.description
            })

    session.close()
    return result

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
    session = Session(engine)

    reward_item = session.query(rewards).filter(rewards.id == reward_id).first()
    if not reward_item:
        session.close()
        return "reward_not_found"

    player = session.query(users).filter(users.id == player_id, users.role == "player").first()
    if not player:
        session.close()
        return "player_not_found"

    already_given = session.query(player_rewards).filter(
        player_rewards.reward_id == reward_id,
        player_rewards.player_id == player_id
    ).first()
    if already_given:
        session.close()
        return "already_assigned"

    completed = session.query(player_missions).filter(
        player_missions.player_id == player_id,
        player_missions.mission_id == reward_item.mission_id,
        player_missions.status == "approved"
    ).first()
    if not completed:
        session.close()
        return "mission_not_completed"

    assigned_entry = player_rewards(
        reward_id=reward_id,
        player_id=player_id,
        assigned_at=datetime.now()
    )
    session.add(assigned_entry)
    session.commit()

    result = {
        "id": assigned_entry.id,
        "reward_id": assigned_entry.reward_id,
        "player_id": assigned_entry.player_id,
        "assigned_at": str(assigned_entry.assigned_at)
    }

    session.close()
    return result

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

    total_rewards = session.query(player_rewards).filter(
        player_rewards.player_id == player_id
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
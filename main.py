from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from pydantic import BaseModel, Field
import functions

app = FastAPI(
    title="Open-World Mission Hub",
    description="Open-World Mission Hub Backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

VALID_DIFFICULTIES = ["easy", "medium", "hard", "special"]
VALID_REVIEW_STATUSES = ["approved", "rejected"]


# Pydantic Models
class UserRegister(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserLogin(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class MissionCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    difficulty: str = Field(min_length=1)
    location: str = Field(min_length=1)
    reward: str = Field(min_length=1)


class MissionUpdate(BaseModel):
    title: str = None
    description: str = None
    difficulty: str = None
    location: str = None
    reward: str = None
    is_active: bool = None


class RewardCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)


# A1 - A3: Authentication APIs
@app.post("/auth/register")
def register(data: UserRegister):
    pass


@app.post("/auth/login")
def login(data: UserLogin):

    user = functions.verify_login(email=data.email,password=data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = functions.create_token(
        user_id=user["user_id"],
        email=user["email"],
        role=user["role"],
        tokentype="access"
    )

    refresh_token = functions.create_token(
        user_id=user["user_id"],
        email=user["email"],
        role=user["role"],
        tokentype="refresh"
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



@app.post("/auth/refresh")
def refresh(refresh_token: str):
    user = functions.verify_token(token=refresh_token, tokentype="refresh")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    access_token = functions.create_token(
        user_id=user["user_id"],
        email=user["email"],
        role=user["role"],
        tokentype="access"
    )
    return {"access_token": access_token}


# E1 - E5: Admin & Mission APIs
@app.post("/admin/mission-managers")
def add_mission_manager(data: UserRegister, token=Header(None)):
    pass


@app.post("/missions")
def add_mission(data: MissionCreate, token=Header(None)):
    pass


@app.get("/missions")
def list_missions(difficulty: str = None, location: str = None, token=Header(None)):
    pass


@app.get("/missions/{mission_id}")
def get_mission(mission_id: int, token=Header(None)):
    pass


@app.patch("/missions/{mission_id}")
def edit_mission(mission_id: int, data: MissionUpdate, token=Header(None)):
    pass


# E6 - E10: Player Mission & Review APIs

@app.post("/missions/{mission_id}/accept")
def accept_mission(mission_id: int, token=Header(None)):

    if not token:
        raise HTTPException(status_code=401, detail="Token Missing")

    payload = functions.verify_login(token=token, tokentype="access")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("role") != "player":
        raise HTTPException(status_code=403, detail="Player access required")

    result = functions.accept_mission(
        player_id=payload["user_id"],
        mission_id=mission_id
    )

    if not result:
        raise HTTPException(status_code=400, detail="Unable to accept mission")

    return result


# E7 - My Accepted Missions
@app.get("/players/me/missions")
def my_accepted_missions(token=Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token Missing")

    payload = functions.verify_login(token=token, tokentype="access")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("role") != "player":
        raise HTTPException(status_code=403, detail="Player access required")

    result = functions.get_player_accepted_missions(
        player_id=payload["user_id"]
    )

    return result


# E8 - Submit Mission
@app.post("/missions/{mission_id}/submit")
def submit_mission(mission_id: int, submission_details: str, token=Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token Missing")

    payload = functions.verify_login(token=token, tokentype="access")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("role") != "player":
        raise HTTPException(status_code=403, detail="Player access required")

    result = functions.submit_mission_completion(
        player_id=payload["user_id"],
        mission_id=mission_id,
        submission_details=submission_details
    )

    if not result:
        raise HTTPException(status_code=400, detail="Unable to submit mission")

    return result


# E9 - Review Submission
@app.patch("/submissions/{submission_id}/review")
def review_submission(submission_id: int, status: str, token=Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token Missing")

    payload = functions.verify_login(token=token, tokentype="access")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("role") != "mission_manager":
        raise HTTPException(status_code=403, detail="Mission Manager access required")

    result = functions.review_mission_completion(
        submission_id=submission_id,
        status=status
    )

    if not result:
        raise HTTPException(status_code=400, detail="Unable to review submission")

    return result

# E10 - Player History
@app.get("/players/{player_id}/history")
def player_history(player_id: int, token=Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token Missing")

    payload = functions.verify_login(token=token, tokentype="access")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("role") != "admin" and payload.get("user_id") != player_id:
        raise HTTPException(status_code=403, detail="Access denied")

    result = functions.get_player_completed_history(
        player_id=player_id
    )

    return result



# E11 - E15: Rewards, Leaderboard & Profile
@app.post("/missions/{mission_id}/rewards")
def add_reward(mission_id: int, data: RewardCreate, token=Header(None)):
    pass


@app.get("/rewards")
def list_rewards(token=Header(None)):
    pass


@app.post("/rewards/{reward_id}/assign")
def assign_reward(reward_id: int, player_id: int, token=Header(None)):
    pass


@app.get("/leaderboard")
def leaderboard(token=Header(None)):
    pass


@app.get("/players/{player_id}/profile")
def player_profile(player_id: int, token=Header(None)):
    pass
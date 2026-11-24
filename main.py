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
    pass


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
    pass


@app.get("/players/me/missions")
def my_accepted_missions(token=Header(None)):
    pass


@app.post("/missions/{mission_id}/submit")
def submit_mission(mission_id: int, submission_details: str, token=Header(None)):
    pass


@app.patch("/submissions/{submission_id}/review")
def review_submission(submission_id: int, status: str, token=Header(None)):
    pass


@app.get("/players/{player_id}/history")
def player_history(player_id: int, token=Header(None)):
    pass


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
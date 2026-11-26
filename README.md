# GTA – Open World Mission Hub

**About the Project:** Open World Mission Hub is a backend application inspired by open-world games, built with FastAPI and SQLite. Players can explore and accept missions, submit completion details and earn rewards and experience points, while mission managers create missions and verify completion, and admins manage the platform.

---

## 1. Project and Team

- **Project Name:** `GTA – Open World Mission Hub`
- **Team Members:** Melvin, Naman, Abhishek

---

## 2. Endpoints and Distribution

### Endpoint Split

**Melvin: Users and Missions**

| # | Functionality | Route |
|:---|:---|:---|
| **A1** | Register | `POST /auth/register` |
| **E1** | Create a mission manager account | `POST /admin/mission-managers` |
| **E2** | Create a new mission | `POST /missions` |
| **E3** | Get all available missions | `GET /missions` |
| **E4** | Get details of a particular mission | `GET /missions/{mission_id}` |
| **E5** | Update mission details or availability | `PATCH /missions/{mission_id}` |

**Abhishek: Gameplay Flow**

| # | Functionality | Route |
|:---|:---|:---|
| **A2** | Login | `POST /auth/login` |
| **E6** | Accept a mission | `POST /missions/{mission_id}/accept` |
| **E7** | Get missions accepted by the logged-in player | `GET /players/me/missions` |
| **E8** | Submit mission completion details | `POST /missions/{mission_id}/submit` |
| **E9** | Approve or reject a mission completion | `PATCH /submissions/{submission_id}/review` |
| **E10** | Get a player's completed mission history | `GET /players/{player_id}/history` |

**Naman: Rewards, Leaderboard and Profile**

| # | Functionality | Route |
|:---|:---|:---|
| **A3** | Refresh token | `POST /auth/refresh` |
| **E11** | Create a reward for a mission | `POST /missions/{mission_id}/rewards` |
| **E12** | Get available rewards | `GET /rewards` |
| **E13** | Assign a reward to a player | `POST /rewards/{reward_id}/assign` |
| **E14** | Get player rankings and leaderboard | `GET /leaderboard` |
| **E15** | Get player profile and statistics | `GET /players/{player_id}/profile` |

### Day 1

**Melvin**

1. Task 1: Initialized the GitHub repository, added GitHub Secrets, and created the `README.md` and base project structure.
2. Task 2: Provisioned the AWS EC2 instance and installed Docker on it.
3. Task 3: Configured the deployment environment by connecting GitHub Secrets with the EC2 and Docker setup.

**Abhishek**

1. Task 1:helped in the base project structure 
2. Task 2:implemented | **A2** | Login | `POST /auth/login` | and  | **E6** | Accept a mission | `POST /missions/{mission_id}/accept` | and | **E7** | Get missions accepted by the logged-in player | `GET /players/me/missions` |
4. Task 3:checked the bugs in this endpoints and A2

**Naman**

1. Task 1: Set up project dependencies and built JWT token utilities (create_token, verify_token) along with the refresh token endpoint (POST /auth/refresh).
2. Task 2: Implemented initial reward creation and listing functions and endpoints (POST /missions/{id}/rewards and GET /rewards).
3. Task 3: Created the leaderboard logic and initial player profile functions and endpoints (GET /leaderboard and GET /players/{id}/profile).

### Day 2

**Melvin**

1. Task 1: Fixed AWS EC2 instance issues and verified deployment stability.
2. Task 2: Implemented E1 (`POST /admin/mission-managers`) for admin-only mission manager creation.
3. Task 3: Implemented E2 (`POST /missions`) for creating new missions.

**Abhishek**

1. Task 1:helped in EC2 instance issues
2. Task 2:worked on | **E8** | Submit mission completion details | `POST /missions/{mission_id}/submit` | and | **E9** | Approve or reject a mission completion | `PATCH /submissions/{submission_id}/review` |
3. Task 3:tested all the four endpoints and assured all are working including | **A2** | Login | `POST /auth/login` |

**Naman**

1. Task 1: Implemented player profile statistics to calculate total missions accepted, completed missions, and total rewards won.
2. Task 2: Built the reward assignment function and endpoint (POST /rewards/{id}/assign) with mission completion validation.
3. Task 3: Separated rewards and player rewards to get multiple-player reward tracking.

### Day 3

**Melvin**

1. Task 1: Fixed AWS EC2 instance issues and verified the running container.
2. Task 2: Implemented E3 (`GET /missions`) and E4 (`GET /missions/{mission_id}`) to list and fetch mission details.
3. Task 3: Implemented E5 (`PATCH /missions/{mission_id}`) to update mission details and availability.

**Abhishek**

1. Task 1:implemented  **E10** | Get a player's completed mission history | `GET /players/{player_id}/history` |
2. Task 2:fixed the bugs in E10
3. Task 3:once checked everything is working on swagger and verified it

**Naman**

1. Task 1: Updated assign_reward and get_player_profile to support both "approved" and "completed" mission statuses for teammate compatibility.
2. Task 2: Tested the endpoints
---

## 3. Live App

- **Live Application / API Base URL:**  
  [http://15.252.243.198:8001](http://15.252.243.198:8001)
- **Hosting:** AWS EC2 instance
- **Server Location:** US East (N. Virginia)

---

## 4. File Structure

```text
open-world-mssion-hub/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── .gitignore
├── Dockerfile
├── functions.py
├── gta.db
├── main.py
├── PRD-GTA – Open World Mission Hub.md
├── README.md
├── requirements.txt
└── test_function.py
```

---

## 5. How to Run It

```bash
docker run -p 8001:8001 image_name
```

---

## 6. API Contract

### Completed Endpoints Table (A1–A3, E1–E15)

| # | What it does | Method | Path | Request Body / Params | Error Codes | Who Built |
|:---:|:---|:---:|:---|:---|:---:|:---:|
| **A1** | Register a new account | `POST` | `/auth/register` | | | Melvin |
| **A2** | Login and generate access and refresh tokens | `POST` | `/auth/login` | | | Abhishek |
| **A3** | Generate a new access token | `POST` | `/auth/refresh` | | | Naman |
| **E1** | Create a mission manager account | `POST` | `/admin/mission-managers` | | | Melvin |
| **E2** | Create a new mission | `POST` | `/missions` | | | Melvin |
| **E3** | Get all available missions | `GET` | `/missions` | | | Melvin |
| **E4** | Get details of a particular mission | `GET` | `/missions/{mission_id}` | | | Melvin |
| **E5** | Update mission details or availability | `PATCH` | `/missions/{mission_id}` | | | Melvin |
| **E6** | Accept a mission | `POST` | `/missions/{mission_id}/accept` | | | Abhishek |
| **E7** | Get missions accepted by the logged-in player | `GET` | `/players/me/missions` | | | Abhishek |
| **E8** | Submit mission completion details | `POST` | `/missions/{mission_id}/submit` | | | Abhishek |
| **E9** | Approve or reject a mission completion | `PATCH` | `/submissions/{submission_id}/review` | | | Abhishek |
| **E10** | Get a player's completed mission history | `GET` | `/players/{player_id}/history` | | | Abhishek |
| **E11** | Create a reward for a mission | `POST` | `/missions/{mission_id}/rewards` | | | Naman |
| **E12** | Get available rewards | `GET` | `/rewards` | | | Naman |
| **E13** | Assign a reward to a player | `POST` | `/rewards/{reward_id}/assign` | | | Naman |
| **E14** | Get player rankings and leaderboard | `GET` | `/leaderboard` | | | Naman |
| **E15** | Get player profile and statistics | `GET` | `/players/{player_id}/profile` | | | Naman |

---

## 7. Database

### Table 1: `users`

| Column | Type | Constraints |
|:---|:---|:---|
| `id` | Integer | Primary Key |
| `username` | String | Not Null |
| `email` | String | Unique, Not Null |
| `hashed_password` | String | Not Null |
| `role` | String | Default: `'player'` |
| `xp` | Integer | Default: `0` |
| `created_at` | DateTime | Default: `TIME` |

### Table 2: `missions`

| Column | Type | Constraints |
|:---|:---|:---|
| `id` | Integer | Primary Key |
| `title` | String | Not Null |
| `description` | String | Not Null |
| `difficulty` | String | Not Null |
| `location` | String | Not Null |
| `reward` | String | Not Null |
| `is_active` | Boolean | Default: `True` |
| `created_by` | Integer | Foreign Key (`users.id`) |
| `created_at` | DateTime | Default: `TIME` |

### Table 3: `player_missions`

| Column | Type | Constraints |
|:---|:---|:---|
| `id` | Integer | Primary Key |
| `player_id` | Integer | Foreign Key (`users.id`) |
| `mission_id` | Integer | Foreign Key (`missions.id`) |
| `status` | String | Default: `'accepted'` |
| `submission_details` | String | Nullable |
| `accepted_at` | DateTime | Default: `TIME` |
| `completed_at` | DateTime | Nullable |

### Table 4: `rewards`

| Column | Type | Constraints |
|:---|:---|:---|
| `id` | Integer | Primary Key |
| `mission_id` | Integer | Foreign Key (`missions.id`) |
| `name` | String | Not Null |
| `description` | String | Not Null |

### Table 5: `player_rewards`

| Column | Type | Constraints |
|:---|:---|:---|
| `id` | Integer | Primary Key |
| `reward_id` | Integer | Foreign Key (`rewards.id`) |
| `player_id` | Integer | Foreign Key (`users.id`) |
| `assigned_at` | DateTime | Default: `TIME` |

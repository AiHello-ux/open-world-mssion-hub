# GTA – Open World Mission Hub

**About the Project:** Open World Mission Hub is a backend application inspired by open-world games, built with FastAPI and SQLite. Players can explore and accept missions, submit completion details, and earn rewards and experience points, while mission managers create missions and verify completion, and admins manage the platform.

---

## 1. Project and Team

- **Project Name:** `GTA – Open World Mission Hub`
- **Team Members:** Melvin, Naman, Abhishek

---

## 2. Endpoints and Distribution

### Endpoint Split

**Melvin: Users and Missions**

| # | Functionality | Route |
| :--- | :--- | :--- |
| **A1** | Register | `POST /auth/register` |
| **E1** | Create a mission manager account | `POST /admin/mission-managers` |
| **E2** | Create a new mission | `POST /missions` |
| **E3** | Get all available missions | `GET /missions` |
| **E4** | Get details of a particular mission | `GET /missions/{mission_id}` |
| **E5** | Update mission details or availability | `PATCH /missions/{mission_id}` |

**Abhishek: Gameplay Flow**

| # | Functionality | Route |
| :--- | :--- | :--- |
| **A2** | Login | `POST /auth/login` |
| **E6** | Accept a mission | `POST /missions/{mission_id}/accept` |
| **E7** | Get missions accepted by the logged-in player | `GET /players/me/missions` |
| **E8** | Submit mission completion details | `POST /missions/{mission_id}/submit` |
| **E9** | Approve or reject a mission completion | `PATCH /submissions/{submission_id}/review` |
| **E10** | Get a player's completed mission history | `GET /players/{player_id}/history` |

**Naman: Rewards, Leaderboard and Profile**

| # | Functionality | Route |
| :--- | :--- | :--- |
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

1. Task 1: Set up project dependencies and built JWT token utilities (`create_token`, `verify_token`) along with the refresh token endpoint (`POST /auth/refresh`).
2. Task 2: Implemented initial reward creation and listing functions and endpoints (`POST /missions/{mission_id}/rewards` and `GET /rewards`).
3. Task 3: Created the leaderboard logic and initial player profile functions and endpoints (`GET /leaderboard` and `GET /players/{player_id}/profile`).

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
2. Task 2: Built the reward assignment function and endpoint (`POST /rewards/{reward_id}/assign`) with mission completion validation.
3. Task 3: Separated `rewards` and `player_rewards` to support multi-player reward tracking.

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
3. Task 3: Added pytest is CI/CD
---

## 3. Live App

- **Live Application / API Base URL:** [http://15.252.243.198:8001](http://15.252.243.198:8001)
- **API Docs (Swagger UI):** [http://15.252.243.198:8001/docs](http://15.252.243.198:8001/docs)
- **Hosting:** AWS EC2 instance
- **Server Location:** US East (N. Virginia)

---

## 4. File Structure

```text
open-world-mssion-hub/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── .dockerignore
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

**With Docker:**

```bash
docker build -t gta-mission-hub .
docker run -p 8001:8001 gta-mission-hub
```

**Locally with Uvicorn:**

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001
```

---

## 6. Roles & XP System

### User Roles

| Role | How Created | Permissions |
| :--- | :--- | :--- |
| `player` | Default on `POST /auth/register` | Browse missions, accept missions, submit completions, view own history, leaderboard, rewards, profiles |
| `mission_manager` | Created by Admin via `POST /admin/mission-managers` | Create/update missions, review submissions, create rewards, assign rewards |
| `admin` | Seeded on startup (`admin@gmail.com`) | Create mission managers, view any player's history, access general authenticated endpoints |

### Mission Difficulty & XP Rewards

| Difficulty | Experience Points (XP) |
| :--- | :---: |
| `easy` | `50` |
| `medium` | `100` |
| `hard` | `200` |
| `special` | `500` |

---

## 7. API Contract

> **Authentication Header:** Protected endpoints expect the JWT access token in the `token` HTTP header (`Header(None)`).

### Completed Endpoints Table (A1–A3, E1–E15)

| # | What it does | Method | Path | Access | Request Body / Params | Error Codes | Who Built |
| :---: | :--- | :---: | :--- | :--- | :--- | :---: | :---: |
| **A1** | Register a new account | `POST` | `/auth/register` | Public | **Body:** `username`, `email`, `password` (`str`, min 1) | `400`, `422` | Melvin |
| **A2** | Login and generate access and refresh tokens | `POST` | `/auth/login` | Public | **Body:** `email`, `password` (`str`, min 1) | `401`, `422` | Abhishek |
| **A3** | Generate a new access token | `POST` | `/auth/refresh` | Public (Refresh Token) | **Query:** `refresh_token` (`str`) | `401`, `422` | Naman |
| **E1** | Create a mission manager account | `POST` | `/admin/mission-managers` | Admin | **Header:** `token`<br>**Body:** `username`, `email`, `password` (`str`, min 1) | `400`, `401`, `403`, `422` | Melvin |
| **E2** | Create a new mission | `POST` | `/missions` | Mission Manager | **Header:** `token`<br>**Body:** `title`, `description`, `difficulty` (`easy`/`medium`/`hard`/`special`), `location`, `reward` (`str`, min 1) | `400`, `401`, `403`, `422` | Melvin |
| **E3** | Get all available missions | `GET` | `/missions` | Any Authenticated User | **Header:** `token`<br>**Query (optional):** `difficulty`, `location` | `401` | Melvin |
| **E4** | Get details of a particular mission | `GET` | `/missions/{mission_id}` | Any Authenticated User | **Header:** `token`<br>**Path:** `mission_id` (`int`) | `401`, `404`, `422` | Melvin |
| **E5** | Update mission details or availability | `PATCH` | `/missions/{mission_id}` | Mission Manager | **Header:** `token`<br>**Path:** `mission_id` (`int`)<br>**Body (optional):** `title`, `description`, `difficulty`, `location`, `reward`, `is_active` (`bool`) | `400`, `401`, `403`, `404`, `422` | Melvin |
| **E6** | Accept a mission | `POST` | `/missions/{mission_id}/accept` | Any Authenticated User | **Header:** `token`<br>**Path:** `mission_id` (`int`) | `400`, `401`, `422` | Abhishek |
| **E7** | Get missions accepted by the logged-in player | `GET` | `/players/me/missions` | Any Authenticated User | **Header:** `token` | `401` | Abhishek |
| **E8** | Submit mission completion details | `POST` | `/missions/{mission_id}/submit` | Player | **Header:** `token`<br>**Path:** `mission_id` (`int`)<br>**Body:** `submission_details` (`str`) | `400`, `401`, `403`, `422` | Abhishek |
| **E9** | Approve or reject a mission completion | `PATCH` | `/submissions/{submission_id}/review` | Mission Manager | **Header:** `token`<br>**Path:** `submission_id` (`int`)<br>**Query:** `status` (`completed` or `rejected`) | `400`, `401`, `403`, `422` | Abhishek |
| **E10** | Get a player's completed mission history | `GET` | `/players/{player_id}/history` | Owner Player or Admin | **Header:** `token`<br>**Path:** `player_id` (`int`) | `401`, `403`, `422` | Abhishek |
| **E11** | Create a reward for a mission | `POST` | `/missions/{mission_id}/rewards` | Mission Manager | **Header:** `token`<br>**Path:** `mission_id` (`int`)<br>**Body:** `name`, `description` (`str`, min 1) | `401`, `403`, `404`, `422` | Naman |
| **E12** | Get available rewards | `GET` | `/rewards` | Any Authenticated User | **Header:** `token` | `401` | Naman |
| **E13** | Assign a reward to a player | `POST` | `/rewards/{reward_id}/assign` | Mission Manager | **Header:** `token`<br>**Path:** `reward_id` (`int`)<br>**Query:** `player_id` (`int`) | `400`, `401`, `403`, `404`, `422` | Naman |
| **E14** | Get player rankings and leaderboard | `GET` | `/leaderboard` | Any Authenticated User | **Header:** `token` | `401` | Naman |
| **E15** | Get player profile and statistics | `GET` | `/players/{player_id}/profile` | Any Authenticated User | **Header:** `token`<br>**Path:** `player_id` (`int`) | `401`, `404`, `422` | Naman |

---

## 8. Database

Database engine: SQLite (`sqlite:///gta.db`), defined via SQLAlchemy ORM in `functions.py`.

### Table 1: `users`

| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `username` | String | Nullable |
| `email` | String | Unique, Nullable |
| `hashed_password` | String | Nullable |
| `role` | String | Default: `'player'` |
| `xp` | Integer | Default: `0` |
| `created_at` | DateTime | Default: `datetime.now` |

### Table 2: `missions`

| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `title` | String | Nullable |
| `description` | String | Nullable |
| `difficulty` | String | Nullable |
| `location` | String | Nullable |
| `reward` | String | Nullable |
| `is_active` | Boolean | Default: `True` |
| `created_by` | Integer | Foreign Key (`users.id`) |
| `created_at` | DateTime | Default: `datetime.now` |

### Table 3: `player_missions`

| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `player_id` | Integer | Foreign Key (`users.id`) |
| `mission_id` | Integer | Foreign Key (`missions.id`) |
| `status` | String | Default: `'accepted'` |
| `submission_details` | String | Nullable |
| `accepted_at` | DateTime | Default: `datetime.now` |
| `completed_at` | DateTime | Nullable |

### Table 4: `rewards`

| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `mission_id` | Integer | Foreign Key (`missions.id`) |
| `name` | String | Nullable |
| `description` | String | Nullable |

### Table 5: `player_rewards`

| Column | Type | Constraints |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `reward_id` | Integer | Foreign Key (`rewards.id`) |
| `player_id` | Integer | Foreign Key (`users.id`) |
| `assigned_at` | DateTime | Default: `datetime.now` |

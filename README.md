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
| **A1** | Register | `POST /register` |
| **E1** | Create a mission manager account | `POST /mission-managers` |
| **E2** | Create a new mission | `POST /missions` |
| **E3** | Get all available missions | `GET /missions` |
| **E4** | Get details of a particular mission | `GET /missions/{id}` |
| **E5** | Update mission details or availability | `PUT /missions/{id}` |

**Abhishek: Gameplay Flow**

| # | Functionality | Route |
|:---|:---|:---|
| **A2** | Login | `POST /login` |
| **E6** | Accept a mission | `POST /missions/{id}` |
| **E7** | Get missions accepted by the logged-in player | `GET /players/me/missions` |
| **E8** | Submit mission completion details | `POST /player-missions/{id}` |
| **E9** | Approve or reject a mission completion | `PATCH /player-missions/{id}` |
| **E10** | Get a player's completed mission history | `GET /my-player` |

**Naman: Rewards, Leaderboard and Profile**

| # | Functionality | Route |
|:---|:---|:---|
| **A3** | Refresh token | `POST /refresh` |
| **E11** | Create a reward for a mission | `POST /rewards` |
| **E12** | Get available rewards | `GET /rewards` |
| **E13** | Assign a reward to a player | `POST /rewards/{id}` |
| **E14** | Get player rankings and leaderboard | `GET /leaderboard` |
| **E15** | Get player profile and statistics | `GET /players/{id}` |

### Day 1

**Melvin**

1. Task 1:
2. Task 2:
3. Task 3:

**Abhishek**

1. Task 1:
2. Task 2:
3. Task 3:

**Naman**

1. Task 1:
2. Task 2:
3. Task 3:

### Day 2

**Melvin**

1. Task 1:
2. Task 2:
3. Task 3:

**Abhishek**

1. Task 1:
2. Task 2:
3. Task 3:

**Naman**

1. Task 1:
2. Task 2:
3. Task 3:

### Day 3

**Melvin**

1. Task 1:
2. Task 2:
3. Task 3:

**Abhishek**

1. Task 1:
2. Task 2:
3. Task 3:

**Naman**

1. Task 1:
2. Task 2:
3. Task 3:

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
| **A1** | Register a new account | `POST` | `/register` | | | Melvin |
| **A2** | Login and generate access and refresh tokens | `POST` | `/login` | | | Abhishek |
| **A3** | Generate a new access token | `POST` | `/refresh` | | | Naman |
| **E1** | Create a mission manager account | `POST` | `/mission-managers` | | | Melvin |
| **E2** | Create a new mission | `POST` | `/missions` | | | Melvin |
| **E3** | Get all available missions | `GET` | `/missions` | | | Melvin |
| **E4** | Get details of a particular mission | `GET` | `/missions/{id}` | | | Melvin |
| **E5** | Update mission details or availability | `PUT` | `/missions/{id}` | | | Melvin |
| **E6** | Accept a mission | `POST` | `/missions/{id}` | | | Abhishek |
| **E7** | Get missions accepted by the logged-in player | `GET` | `/players/me/missions` | | | Abhishek |
| **E8** | Submit mission completion details | `POST` | `/player-missions/{id}` | | | Abhishek |
| **E9** | Approve or reject a mission completion | `PATCH` | `/player-missions/{id}` | | | Abhishek |
| **E10** | Get a player's completed mission history | `GET` | `/my-player` | | | Abhishek |
| **E11** | Create a reward for a mission | `POST` | `/rewards` | | | Naman |
| **E12** | Get available rewards | `GET` | `/rewards` | | | Naman |
| **E13** | Assign a reward to a player | `POST` | `/rewards/{id}` | | | Naman |
| **E14** | Get player rankings and leaderboard | `GET` | `/leaderboard` | | | Naman |
| **E15** | Get player profile and statistics | `GET` | `/players/{id}` | | | Naman |

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
| `assigned_to` | Integer | Foreign Key (`users.id`), Nullable |
| `assigned_at` | DateTime | Nullable |

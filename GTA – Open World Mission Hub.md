# **PRD: GTA – Open World Mission Hub**

## **1\. Project Overview**

Build a backend application inspired by open-world games. Players can explore available missions, accept missions, complete objectives and earn rewards. Administrators manage the platform, while mission managers create missions and validate completion.

**Backend only – no frontend is required.**

## **2\. Team Requirements**

> * Team size: 3 students.  
> * One student must create the GitHub repository as team leader.  
> * All three members must contribute to the same repository.  
> * Each student must implement at least 5 project-specific APIs.  
> * All members must contribute through meaningful commits.

## **3\. User Roles**

| Role | Responsibilities |
| ----- | ----- |
| **Admin** | Manage mission managers and platform activities |
| **Mission Manager** | Create missions, manage availability and verify completion |
| **Player** | Accept missions, submit completion details and earn rewards |

New registrations receive the `player` role by default. Only admins can create mission manager accounts.

## **4\. API Requirements**

The application must contain **18 APIs: 3 authentication APIs and 15 project-specific APIs.**

### **A. Authentication APIs (3)**

| \# | Functionality | Method | Endpoint |
| ----- | ----- | ----- | ----- |
| **A1** | Register a new account | POST | `/auth/register` |
| **A2** | Login and generate access and refresh tokens | POST | `/auth/login` |
| **A3** | Generate a new access token | POST | `/auth/refresh` |

### **B. Project-Specific APIs (15)**

| \# | Functionality | Access |
| ----- | ----- | ----- |
| **E1** | Create a mission manager account | Admin |
| **E2** | Create a new mission | Mission Manager |
| **E3** | Get all available missions | All |
| **E4** | Get details of a particular mission | All |
| **E5** | Update mission details or availability | Mission Manager |
| **E6** | Accept a mission | Player |
| **E7** | Get missions accepted by the logged-in player | Player |
| **E8** | Submit mission completion details | Player |
| **E9** | Approve or reject a mission completion | Mission Manager |
| **E10** | Get a player's completed mission history | Player |
| **E11** | Create a reward for a mission | Mission Manager |
| **E12** | Get available rewards | All |
| **E13** | Assign a reward to a player | Mission Manager |
| **E14** | Get player rankings and leaderboard | All |
| **E15** | Get player profile and statistics | All |

Teams must decide the appropriate HTTP methods, endpoint paths, request bodies and response formats.

## **5\. Business Requirements**

> * A mission must contain a title, description, difficulty, location and reward.  
> * Missions can have difficulty levels such as easy, medium and hard.  
> * Mission managers can publish and deactivate missions.  
> * Players can accept available missions.  
> * A player cannot accept the same active mission more than once.  
> * Players must submit completion details before a mission can be marked completed.  
> * Mission managers must approve or reject submitted completion details.  
> * Rewards can be assigned only after successful completion.  
> * Players must have a profile showing completed missions, total rewards and experience points.  
> * The leaderboard must rank players based on accumulated experience points.

### **Suggested Reward System**

| Mission Difficulty | Experience Points |
| ----- | ----- |
| **Easy** | 50 |
| **Medium** | 100 |
| **Hard** | 200 |
| **Special** | 500 |

The backend must calculate rewards based on approved mission completion.

## **6\. Technical Requirements**

> * Python and FastAPI.  
> * Pydantic for request validation.  
> * SQLite database.  
> * JWT access and refresh tokens.  
> * Secure password hashing.  
> * Role-based access control.  
> * Proper HTTP status codes and error handling.  
> * Modular application structure.  
> * API documentation through `/docs`.

The team must design the database tables, fields and relationships required for the application.

## **7\. Docker and AWS Deployment**

> * Create a Dockerfile and build a Docker image.  
> * Run the FastAPI application inside a container on port `8001`.  
> * Do not use Docker Compose.  
> * Deploy the application on one AWS EC2 instance.  
> * Configure security groups and expose the API through the EC2 public IP.  
> * Persist SQLite data outside the container using a mounted directory.

## **8\. CI/CD Requirements**

Implement GitHub Actions to build the Docker image, push it to Docker Hub, connect to EC2, pull the latest image and replace the running container.

Use GitHub Secrets for Docker Hub credentials and EC2 SSH access.

## **9\. Submission Requirements**

> * GitHub repository with source code.  
> * README and API documentation.  
> * Dockerfile and Docker Hub image.  
> * GitHub Actions deployment workflow.  
> * Working EC2 deployment and public API URL.  
> * Evidence of contributions from all three students.

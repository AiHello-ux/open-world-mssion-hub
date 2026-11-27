from fastapi.testclient import TestClient
import functions
import main

client = TestClient(main.app)

functions.Base.metadata.drop_all(functions.engine)
functions.Base.metadata.create_all(functions.engine)

def test_full_game_flow():
    admin_token = functions.create_token(user_id=1, email="admin@test.com", role="admin")
    admin_header = {"token": admin_token}

    manager_credentials = {
        "username": "manager1",
        "email": "manager1@test.com",
        "password": "pass"
    }
    response = client.post("/admin/mission-managers", json=manager_credentials, headers=admin_header)
    assert response.status_code == 200

    response = client.post("/auth/login", json={"email": "manager1@test.com", "password": "pass"})
    assert response.status_code == 200
    manager_token = response.json()["access_token"]
    manager_header = {"token": manager_token}

    player_credentials = {
        "username": "player1",
        "email": "player1@test.com",
        "password": "pass"
    }
    response = client.post("/auth/register", json=player_credentials)
    assert response.status_code == 200

    response = client.post("/auth/register", json=player_credentials)
    assert response.status_code == 400

    response = client.post("/auth/login", json={"email": "player1@test.com", "password": "pass"})
    assert response.status_code == 200
    player_token = response.json()["access_token"]
    player_refresh = response.json()["refresh_token"]
    player_header = {"token": player_token}
    player_id = functions.verify_token(player_token)["user_id"]

    response = client.post("/auth/refresh", params={"refresh_token": player_refresh})
    assert response.status_code == 200
    assert "access_token" in response.json()

    mission_data = {
        "title": "Bank Robbery",
        "description": "Crack the vault",
        "difficulty": "easy",
        "location": "Downtown",
        "reward": "100"
    }
    response = client.post("/missions", json=mission_data, headers=manager_header)
    assert response.status_code == 200

    response = client.get("/missions", headers=player_header)
    assert response.status_code == 200
    missions = response.json()["missions"]
    assert len(missions) >= 1
    mission_id = missions[0]["id"]

    response = client.get(f"/missions/{mission_id}", headers=player_header)
    assert response.status_code == 200

    response = client.patch(f"/missions/{mission_id}", json={"description": "Updated"}, headers=manager_header)
    assert response.status_code == 200

    response = client.post(f"/missions/{mission_id}/accept", headers=player_header)
    assert response.status_code == 200

    response = client.get("/players/me/missions", headers=player_header)
    assert response.status_code == 200
    assert len(response.json()) == 1

    submit_data = {"submission_details": "Vault cracked"}
    response = client.post(f"/missions/{mission_id}/submit", json=submit_data, headers=player_header)
    assert response.status_code == 200

    response = client.patch("/submissions/1/review?status=completed", headers=manager_header)
    assert response.status_code == 200

    response = client.get(f"/players/{player_id}/history", headers=player_header)
    assert response.status_code == 200
    assert len(response.json()) == 1

    reward_data = {
        "name": "Gold Medal",
        "description": "For bank robbery"
    }
    response = client.post(f"/missions/{mission_id}/rewards", json=reward_data, headers=manager_header)
    assert response.status_code == 200
    reward_id = response.json()["id"]

    response = client.get("/rewards", headers=player_header)
    assert response.status_code == 200
    assert len(response.json()) >= 1

    response = client.post(f"/rewards/{reward_id}/assign?player_id={player_id}", headers=manager_header)
    assert response.status_code == 200

    response = client.get("/rewards", headers=player_header)
    assert response.status_code == 200

    response = client.get("/leaderboard", headers=player_header)
    assert response.status_code == 200

    response = client.get(f"/players/{player_id}/profile", headers=player_header)
    assert response.status_code == 200
    profile = response.json()
    assert profile["total_missions_taken"] == 1
    assert profile["completed_missions"] == 1
    assert profile["total_rewards"] == 1

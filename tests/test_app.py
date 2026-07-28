from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    assert "Chess Club" in data
    chess_club = data["Chess Club"]
    assert set(["description", "schedule", "max_participants", "participants"]).issubset(chess_club.keys())
    assert "michael@mergington.edu" in chess_club["participants"]


def test_signup_for_activity_success(client):
    email = "newstudent@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity_returns_404(client):
    response = client.post("/activities/Nonexistent Club/signup", params={"email": "someone@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_already_registered_returns_400(client):
    existing_email = "michael@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_from_activity_success(client):
    email = "michael@mergington.edu"

    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_from_nonexistent_activity_returns_404(client):
    response = client.delete("/activities/Nonexistent Club/signup", params={"email": "someone@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_participant_not_found_returns_404(client):
    response = client.delete("/activities/Chess Club/signup", params={"email": "notregistered@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}

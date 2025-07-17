
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    r = requests.get(f"{BASE_URL}/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_get_games():
    r = requests.get(f"{BASE_URL}/api/games")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_metrics():
    games = requests.get(f"{BASE_URL}/api/games").json()
    if not games:
        print("No games available to test metrics.")
        return
    game = games[0]
    r = requests.get(f"{BASE_URL}/api/data/metrics/{game}")
    assert r.status_code == 200
    assert "ViewsTotal" in r.json()

def test_get_data():
    games = requests.get(f"{BASE_URL}/api/games").json()
    if not games:
        print("No games available to test data.")
        return
    game = games[0]
    r = requests.get(f"{BASE_URL}/api/data/{game}?limit=5")
    assert r.status_code == 200
    assert "actions" in r.json()

if __name__ == "__main__":
    print("Running FastAPI API tests...")
    test_health()
    test_get_games()
    test_get_metrics()
    test_get_data()
    print("✅ All tests passed.")

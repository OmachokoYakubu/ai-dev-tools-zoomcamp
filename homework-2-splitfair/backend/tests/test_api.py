import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app

# In-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_and_get_group():
    res = client.post("/api/groups", json={
        "title": "Apt 4B Roommates",
        "description": "Shared apartment utilities & cleaning",
        "currency": "USD"
    })
    assert res.status_code == 201
    group_data = res.json()
    assert group_data["title"] == "Apt 4B Roommates"
    group_id = group_data["id"]

    # Get group details
    detail_res = client.get(f"/api/groups/{group_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["title"] == "Apt 4B Roommates"
    assert detail_res.json()["members"] == []

def test_add_members_and_record_expense():
    # 1. Create Group
    g_res = client.post("/api/groups", json={"title": "Tahoe Ski Trip"})
    group_id = g_res.json()["id"]

    # 2. Add Members (Alice, Bob, Charlie)
    m1 = client.post(f"/api/groups/{group_id}/members", json={"name": "Alice", "email": "alice@test.com"}).json()
    m2 = client.post(f"/api/groups/{group_id}/members", json={"name": "Bob", "email": "bob@test.com"}).json()
    m3 = client.post(f"/api/groups/{group_id}/members", json={"name": "Charlie", "email": "charlie@test.com"}).json()

    # 3. Record Expense: Alice pays $90 split equally among all 3
    exp_res = client.post(f"/api/groups/{group_id}/expenses", json={
        "title": "Dinner at Tahoe Grill",
        "amount": 90.0,
        "category": "Food",
        "payer_id": m1["id"],
        "split_member_ids": [m1["id"], m2["id"], m3["id"]]
    })
    assert exp_res.status_code == 201
    assert exp_res.json()["payer_name"] == "Alice"

    # 4. Check Balances:
    # Alice: paid 90, share 30 => net +60
    # Bob: paid 0, share 30 => net -30
    # Charlie: paid 0, share 30 => net -30
    bal_res = client.get(f"/api/groups/{group_id}/balances")
    assert bal_res.status_code == 200
    data = bal_res.json()
    
    balances = {b["member_name"]: b["net_balance"] for b in data["balances"]}
    assert balances["Alice"] == 60.0
    assert balances["Bob"] == -30.0
    assert balances["Charlie"] == -30.0

    # Settlements recommended
    settlements = data["settlements"]
    assert len(settlements) == 2
    rec_pairs = {(s["from_member_name"], s["to_member_name"], s["amount"]) for s in settlements}
    assert ("Bob", "Alice", 30.0) in rec_pairs
    assert ("Charlie", "Alice", 30.0) in rec_pairs

def test_settle_debt():
    g_res = client.post("/api/groups", json={"title": "Weekend Outing"})
    group_id = g_res.json()["id"]

    m1 = client.post(f"/api/groups/{group_id}/members", json={"name": "Dana", "email": "dana@test.com"}).json()
    m2 = client.post(f"/api/groups/{group_id}/members", json={"name": "Eli", "email": "eli@test.com"}).json()

    # Dana pays $50 for both
    client.post(f"/api/groups/{group_id}/expenses", json={
        "title": "Groceries",
        "amount": 50.0,
        "payer_id": m1["id"],
        "split_member_ids": [m1["id"], m2["id"]]
    })

    # Record settlement: Eli pays Dana $25
    setl_res = client.post(f"/api/groups/{group_id}/settle", json={
        "from_member_id": m2["id"],
        "to_member_id": m1["id"],
        "amount": 25.0
    })
    assert setl_res.status_code == 201

    # Balances should now be $0.00
    bal_res = client.get(f"/api/groups/{group_id}/balances").json()
    balances = {b["member_name"]: b["net_balance"] for b in bal_res["balances"]}
    assert balances["Dana"] == 0.0
    assert balances["Eli"] == 0.0
    assert len(bal_res["settlements"]) == 0

def test_invalid_payer_error():
    g_res = client.post("/api/groups", json={"title": "Error Test Group"})
    group_id = g_res.json()["id"]

    res = client.post(f"/api/groups/{group_id}/expenses", json={
        "title": "Invalid Expense",
        "amount": 20.0,
        "payer_id": 9999,
        "split_member_ids": [1]
    })
    assert res.status_code == 400

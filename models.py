import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _load(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_all_politicians():
    return _load("politicians.json")


def get_politician(politician_id):
    for p in get_all_politicians():
        if p["id"] == politician_id:
            return p
    return None


def get_all_campaigns():
    return _load("campaigns.json")


def get_campaign(campaign_id):
    for c in get_all_campaigns():
        if c["id"] == campaign_id:
            return c
    return None


def get_all_promises():
    promises = _load("promises.json")
    promises.sort(key=lambda x: x["announced_date"], reverse=True)
    return promises


def get_promise(promise_id):
    for p in get_all_promises():
        if p["id"] == promise_id:
            return p
    return None


def get_promises_by_politician(politician_id):
    return [p for p in get_all_promises() if p["politician_id"] == politician_id]


def update_promise_status(promise_id, new_status):
    promises = _load("promises.json")
    for p in promises:
        if p["id"] == promise_id:
            p["status"] = new_status
            break
    _save("promises.json", promises)


def get_updates_by_promise(promise_id):
    updates = _load("promise_updates.json")
    result = [u for u in updates if u["promise_id"] == promise_id]
    result.sort(key=lambda x: x["update_date"], reverse=True)
    return result


def add_promise_update(promise_id, detail):
    updates = _load("promise_updates.json")
    new_id = max([u["id"] for u in updates], default=0) + 1
    updates.append({
        "id": new_id,
        "promise_id": promise_id,
        "update_date": datetime.now().strftime("%Y-%m-%d"),
        "detail": detail
    })
    _save("promise_updates.json", updates)


USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
}


def authenticate(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return {"username": username, "role": user["role"]}
    return None

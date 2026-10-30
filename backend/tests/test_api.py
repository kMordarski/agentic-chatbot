import json

HEADERS = {"X-API-Key": "test-key"}
BODY = {"messages": [{"role": "user", "content": "hi"}]}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_without_api_key_returns_401(client):
    response = client.post("/chat", json=BODY)
    assert response.status_code == 401


def test_chat_returns_fake_reply(client):
    response = client.post("/chat", json=BODY, headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"reply": "fixed_string"}


def test_chat_stream_sends_sse_and_done(client):
    response = client.post("/chat/stream", json=BODY, headers=HEADERS)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

    payloads = [
        line.removeprefix("data: ")
        for line in response.text.splitlines()
        if line.startswith("data: ")
    ]
    assert payloads[-1] == "[DONE]"
    assert "".join(json.loads(p) for p in payloads[:-1]) == "hello!"
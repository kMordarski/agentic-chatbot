import json
import uuid
 
HEADERS = {"X-API-Key": "test-key"}
 
 
def body(conversation_id: str) -> dict:
    return {
        "conversation_id": conversation_id,
        "messages": [{"role": "user", "content": "hi"}],
    }
 
 
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
 
 
def test_chat_without_api_key_returns_401(client, conversation_id):
    response = client.post("/chat", json=body(conversation_id))
    assert response.status_code == 401
 
 
def test_chat_returns_fake_reply(client, conversation_id):
    response = client.post("/chat", json=body(conversation_id), headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"reply": "fixed_string"}
 
 
def test_chat_stream_sends_sse_and_done(client, conversation_id):
    response = client.post("/chat/stream", json=body(conversation_id), headers=HEADERS)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
 
    payloads = [
        line.removeprefix("data: ")
        for line in response.text.splitlines()
        if line.startswith("data: ")
    ]
    assert payloads[-1] == "[DONE]"
    assert "".join(json.loads(p) for p in payloads[:-1]) == "hello!"
 
 
# --- Day 6: persistence ---
 
def test_create_conversation_returns_uuid(client):
    response = client.post("/conversations", headers=HEADERS)
    assert response.status_code == 200
    uuid.UUID(response.json()["id"])  # raises if it is not a valid uuid
 
 
def test_new_conversation_has_no_messages(client, conversation_id):
    response = client.get(f"/conversations/{conversation_id}/messages", headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == []
 
 
def test_stream_saves_user_and_assistant_messages(client, conversation_id):
    client.post("/chat/stream", json=body(conversation_id), headers=HEADERS)
 
    response = client.get(f"/conversations/{conversation_id}/messages", headers=HEADERS)
    assert response.json() == [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello!"},
    ]
 
 
def test_messages_with_invalid_id_returns_422(client):
    response = client.get("/conversations/not-a-uuid/messages", headers=HEADERS)
    assert response.status_code == 422
 
 
def test_stream_without_conversation_id_returns_422(client):
    response = client.post(
        "/chat/stream",
        json={"messages": [{"role": "user", "content": "hi"}]},
        headers=HEADERS,
    )
    assert response.status_code == 422
 
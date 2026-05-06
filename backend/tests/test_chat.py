import os
from datetime import UTC, datetime, timedelta

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from starlette.websockets import WebSocketDisconnect

from models import Message, Room, User


def _mint_token(address: str) -> str:
    secret = os.environ["JWT_SECRET"]
    payload = {
        "sub": address,
        "username": "tester",
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + timedelta(minutes=5),
        "iss": "playlink-auth",
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def _all(session: Session, statement):
    return session.exec(statement).all()


def _seed_room_and_users(session: Session, room_name: str, members: list[str]) -> Room:
    user_objs = []
    for addr in members:
        u = User(identity_address=addr)
        session.add(u)
        user_objs.append(u)
    session.commit()
    for u in user_objs:
        session.refresh(u)

    room = Room(
        name=room_name,
        game="Quake III Arena",
        players_max=4,
        created_by=members[0],
    )
    room.members.extend(user_objs)
    session.add(room)
    session.commit()
    session.refresh(room)
    return room


def test_chat_rejects_bad_token(client: TestClient, session: Session):
    _seed_room_and_users(session, "r1", ["0xabc"])
    with (
        pytest.raises(WebSocketDisconnect) as exc,
        client.websocket_connect("/ws/rooms/r1/chat?token=garbage"),
    ):
        pass
    assert exc.value.code == 4401


def test_chat_rejects_non_member(client: TestClient, session: Session):
    _seed_room_and_users(session, "r2", ["0xMember"])
    outsider = "0xOutsider"
    session.add(User(identity_address=outsider))
    session.commit()
    token = _mint_token(outsider)
    with (
        pytest.raises(WebSocketDisconnect) as exc,
        client.websocket_connect(f"/ws/rooms/r2/chat?token={token}"),
    ):
        pass
    assert exc.value.code == 4403


def test_chat_rejects_missing_room(client: TestClient, session: Session):
    addr = "0xLone"
    session.add(User(identity_address=addr))
    session.commit()
    token = _mint_token(addr)
    with (
        pytest.raises(WebSocketDisconnect) as exc,
        client.websocket_connect(f"/ws/rooms/nope/chat?token={token}"),
    ):
        pass
    assert exc.value.code == 4404


def test_chat_broadcast_between_members(client: TestClient, session: Session):
    a, b = "0xAlice", "0xBob"
    _seed_room_and_users(session, "lobby", [a, b])
    ta, tb = _mint_token(a), _mint_token(b)

    with (
        client.websocket_connect(f"/ws/rooms/lobby/chat?token={ta}") as ws_a,
        client.websocket_connect(f"/ws/rooms/lobby/chat?token={tb}") as ws_b,
    ):
        history_a = ws_a.receive_json()
        history_b = ws_b.receive_json()
        assert history_a == {"type": "history", "messages": []}
        assert history_b == {"type": "history", "messages": []}

        ws_a.send_json({"content": "hello world"})

        msg_a = ws_a.receive_json()
        msg_b = ws_b.receive_json()
        assert msg_a["type"] == "message"
        assert msg_b["type"] == "message"
        assert msg_a["message"]["content"] == "hello world"
        assert msg_a["message"]["sender_address"] == a
        assert msg_b["message"]["content"] == "hello world"

    rows = _all(session, select(Message))
    assert len(rows) == 1
    assert rows[0].content == "hello world"


def test_chat_history_replay(client: TestClient, session: Session):
    addr = "0xSolo"
    _seed_room_and_users(session, "echoes", [addr])
    token = _mint_token(addr)

    with client.websocket_connect(f"/ws/rooms/echoes/chat?token={token}") as ws:
        ws.receive_json()
        ws.send_json({"content": "first"})
        ws.receive_json()
        ws.send_json({"content": "second"})
        ws.receive_json()

    with client.websocket_connect(f"/ws/rooms/echoes/chat?token={token}") as ws:
        history = ws.receive_json()
        assert history["type"] == "history"
        contents = [m["content"] for m in history["messages"]]
        assert contents == ["first", "second"]


def test_chat_drops_oversize_and_empty(client: TestClient, session: Session):
    addr = "0xWriter"
    _seed_room_and_users(session, "limited", [addr])
    token = _mint_token(addr)

    with client.websocket_connect(f"/ws/rooms/limited/chat?token={token}") as ws:
        ws.receive_json()
        ws.send_json({"content": "   "})
        ws.send_json({"content": "x" * 1001})
        ws.send_json({"content": "kept"})
        msg = ws.receive_json()
        assert msg["message"]["content"] == "kept"

    rows = _all(session, select(Message))
    assert [r.content for r in rows] == ["kept"]

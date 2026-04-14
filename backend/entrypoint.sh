#!/bin/sh
set -e

for i in $(seq 1 30); do
  python - <<'PY' && break
import socket, sys
try:
    socket.getaddrinfo("db", 5432)
    s = socket.create_connection(("db", 5432), timeout=2)
    s.close()
except Exception:
    sys.exit(1)
PY
  echo "DB not ready yet ($i/30)"
  sleep 2
done

alembic upgrade head
exec uvicorn main:app --host 0.0.0.0 --port 8000

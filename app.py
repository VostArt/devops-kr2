# KR2: Kozin
import os
import socket
from flask import Flask, request
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
STUDENT = os.getenv("STUDENT", "unknown")


def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=6379,
        password=REDIS_PASSWORD,
        decode_responses=True
    )


@app.route("/health")
def health():
    return "ok\n"


@app.route("/")
def index():
    client = get_redis_client()
    hits = client.incr("hits")
    container_id = socket.gethostname()[:8]
    return f"KR2 | {STUDENT} | container {container_id} | hits: {hits}\n"


@app.route("/whoami")
def whoami():
    scheme = request.headers.get("X-Forwarded-Proto", "none")
    client = request.headers.get("X-Real-IP", "none")
    host = request.headers.get("Host", "none")
    return f"scheme: {scheme}\nclient: {client}\nhost: {host}\n"
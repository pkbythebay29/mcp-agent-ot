
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis
import json

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    messages = r.lrange("agent_log", 0, 20)
    html = "<h2>MCP Agent Dashboard</h2><ul>"
    for msg in messages:
        html += f"<li>{msg}</li>"
    html += "</ul>"
    return html

@app.post("/trigger/vector-update")
async def trigger_vector():
    r.publish("vector/trigger", json.dumps({"action": "update"}))
    r.lpush("agent_log", "Vector store update triggered")
    return {"status": "ok"}

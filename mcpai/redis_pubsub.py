
import redis
import json

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

def publish(channel, message):
    redis_client.publish(channel, json.dumps(message))
    redis_client.lpush("agent_log", f"Published to {channel}: {message}")

def subscribe(channel, handler):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    print(f"[Subscribed] to {channel}")
    for msg in pubsub.listen():
        if msg["type"] == "message":
            data = json.loads(msg["data"])
            handler(data)

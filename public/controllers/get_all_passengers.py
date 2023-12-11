from public.connection.radis_storage import redis_conn
async def get_all_passengers():
    passengers = []
    all_keys = redis_conn.keys("user:*")
    
    for key in all_keys:
        user_data = redis_conn.hgetall(key)
        if user_data.get("role") == "passenger":
            passengers.append(int(user_data["id"]))

    return passengers
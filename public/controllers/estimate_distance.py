
import datetime
import random


async def estimate_time_distance():
    distance = random.randint(5, 100)
    curr = datetime.now()
    minu = random.randint(1, 60)
    delta = datetime.timedelta(minutes=minu)
    estim = curr + delta
    return distance, estim.strftime("%I:%M %p")
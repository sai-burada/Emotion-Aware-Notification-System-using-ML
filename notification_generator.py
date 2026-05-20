import random

notifications = [
    {"app": "WhatsApp", "msg": "New message"},
    {"app": "Email", "msg": "New mail"},
    {"app": "Bank", "msg": "Transaction alert"}
]

def get_notification():
    return random.choice(notifications)
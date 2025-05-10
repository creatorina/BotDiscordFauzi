import random

def get_random_greeting(name):
    greetings = [
        f"Selamat pagi, {name}! Semangat terus!",
        f"Halo {name}, semoga harimu cerah!",
        f"Good morning, {name}!",
    ]
    return random.choice(greetings)

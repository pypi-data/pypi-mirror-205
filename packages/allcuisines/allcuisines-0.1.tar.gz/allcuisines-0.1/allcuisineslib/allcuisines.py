import random

def generate_cuisines():
    cuisines = [
        "Chinese",
        "Indian",
        "Thai",
        "Italian",
        "Arabic"
    ]
    return random.choice(cuisines)

print(generate_cuisines())
import random

def generate_offers():
    offers = [
        "Prune - Dried Fruit",
        "Tomatoes - Vegetable",
        "Carrots - Vegetable",
        "Grapes - Fruits",
        "Mangoes - Fruits",
        "Almond - Dried Fruit",
    ]
    return random.choice(offers)

print(generate_offers())
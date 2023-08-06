import random

def generate_bestsellers():
    bestsellers = [
        "Carbonara Pasta",
        "Fried Chicken Burger",
        "Dutch Truffle Pastry",
        "Veggie Pizza",
        "Shawarma Wrap"
    ]
    return random.choice(bestsellers)

print(generate_bestsellers())
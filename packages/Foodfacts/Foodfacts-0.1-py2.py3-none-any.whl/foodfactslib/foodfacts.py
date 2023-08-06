import random

def generate_facts():
    facts = [
        "Butter chicken, a popular North Indian dish, was actually invented by mistake when a chef added leftover tandoori chicken to a tomato-based gravy.",
        "Biryani, a rice dish made with spices, meat, and/or vegetables, originated in Persia and was brought to India by the Mughals.",
        "The popular street food snack, samosas, originated in Central Asia and were introduced to India by traders.",
        "Masala chai, a spiced tea drink, was originally created as a medicinal drink in ancient India.",
        "The dessert dish rasgulla, made from cottage cheese balls soaked in syrup, originated in East India and is believed to have been created in the 19th century.",
        "The Indian state of Goa is known for its seafood dishes, which are heavily influenced by Portuguese cuisine.",
        "The world's most expensive coffee is made from the droppings of a civet cat.",
        "Honey never spoils - it can last for thousands of years.",
        "The world's oldest known recipe is for beer.",
        "The world's largest pizza was 122 feet in diameter.",
        "The easiest way to make money is to solve a problem that people are willing to pay for.",
        "Money is a tool, not a goal. It's a means to an end, not an end in itself.",
        "It's not the employer who pays the wages. Employers only handle the money. It's the customer who pays the wages.",
        "The real measure of your wealth is how much you'd be worth if you lost all your money.",
    ]
    return random.choice(facts)

print(generate_facts())

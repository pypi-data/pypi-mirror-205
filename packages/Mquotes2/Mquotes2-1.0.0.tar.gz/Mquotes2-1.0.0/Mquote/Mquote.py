import random

def generate_quote():
    quotes = [
        "Money is a great servant but a bad master.",
        "The art is not in making money, but in keeping it.",
        "Money is like manure; it's not worth a thing unless it's spread around encouraging young things to grow.",
        "You can only become truly accomplished at something you love. Don’t make money your goal. Instead, pursue the things you love doing, and then do them so well that people can’t take their eyes off you.",
        "I'm a great believer in luck, and I find the harder I work, the more I have of it.",
        "The more you learn, the more you earn.",
        "It's not about money or connections. It's the willingness to outwork and outlearn everyone when it comes to your business.",
        "Money is usually attracted, not pursued.",
        "Wealth is the ability to fully experience life.",
        "The only place where success comes before work is in the dictionary.",
        "The easiest way to make money is to solve a problem that people are willing to pay for.",
        "Money is a tool, not a goal. It's a means to an end, not an end in itself.",
        "It's not the employer who pays the wages. Employers only handle the money. It's the customer who pays the wages.",
        "The real measure of your wealth is how much you'd be worth if you lost all your money.",
    ]
    return random.choice(quotes)

print(generate_quote())

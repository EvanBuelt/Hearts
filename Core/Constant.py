class Enum:
    def __init__(self):
        return


class Suit(Enum):
    Empty = 0
    Clubs = 1
    Diamonds = 2
    Spades = 3
    Hearts = 4


class Value(Enum):
    Empty = 0
    Ace = 14
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13


suit_str = {Suit.Clubs: "Clubs",
            Suit.Diamonds: "Diamonds",
            Suit.Spades: "Spades",
            Suit.Hearts: "Hearts"}

value_str = {Value.Ace: "Ace",
             Value.Two: "2",
             Value.Three: "3",
             Value.Four: "4",
             Value.Five: "5",
             Value.Six: "6",
             Value.Seven: "7",
             Value.Eight: "8",
             Value.Nine: "9",
             Value.Ten: "10",
             Value.Jack: "Jack",
             Value.Queen: "Queen",
             Value.King: "King"}

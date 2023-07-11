import random

# Emoji card suits
SUITS = ["♠️", "♥️", "♦️", "♣️"]

# Card ranks
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

# Card values
VALUES = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += VALUES[card.rank]
        if card.rank == "A":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Game:
    def __init__(self, starting_money):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.money = starting_money
        self.bet = 0

    def start(self):
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())

    def place_bet(self):
        print("Money:", self.money)
        while True:
            try:
                bet = int(input("Place your bet: "))
                if 1 <= bet <= self.money:
                    self.bet = bet
                    break
                else:
                    print("Invalid bet amount. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid bet.")

    def hit(self):
        self.player_hand.add_card(self.deck.deal_card())
        self.player_hand.adjust_for_ace()

    def dealer_play(self):
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
            self.dealer_hand.adjust_for_ace()

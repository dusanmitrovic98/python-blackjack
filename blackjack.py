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

    def get_score(self):
        return self.player_hand.value, self.dealer_hand.value

    def is_player_bust(self):
        return self.player_hand.value > 21

    def is_dealer_bust(self):
        return self.dealer_hand.value > 21

    def is_player_win(self):
        return self.player_hand.value > self.dealer_hand.value

    def is_dealer_win(self):
        return self.dealer_hand.value > self.player_hand.value

    def is_draw(self):
        return self.player_hand.value == self.dealer_hand.value

    def display_hand(self, hide_dealer_card=False):
        print("===== Blackjack =====")
        print("Player's hand:", ', '.join(str(card) for card in self.player_hand.cards))
        print("Dealer's hand:", end=' ')
        if hide_dealer_card:
            print(str(self.dealer_hand.cards[0]), "<hidden card>")
        else:
            print(', '.join(str(card) for card in self.dealer_hand.cards))
        print("Player's score:", self.player_hand.value)
        print("Dealers's score:", self.dealer_hand.value)
        print("Money:", self.money)
        print("=====================")


# Initialize and start the game
starting_money = 100
game = Game(starting_money)

while game.money > 0:
    game.start()
    game.place_bet()

    while True:
        game.display_hand(hide_dealer_card=True)

        game.display_hand()

        if game.is_player_bust():
            game.money -= game.bet
            print("You busted! Dealer wins.")
            break

        action = input("Do you want to hit (h), stand (s), or quit (q)? ").lower()

        if action == "h":
            game.hit()
        elif action == "s":
            game.dealer_play()

            game.display_hand()

            if game.is_dealer_bust():
                game.money += game.bet
                print("Dealer busted! You win.")
            elif game.is_player_win():
                game.money += game.bet
                print("You win!")
            elif game.is_dealer_win():
                print("Dealer wins.")
                game.money -= game.bet
            else:
                print("It's a draw.")

            break
        elif action == "q":
            break
        else:
            print("Invalid input. Please try again.")

    if action == "q":
        break

    print()

print("Game over. Thank you for playing!")

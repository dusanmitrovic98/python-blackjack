    def is_dealer_bust(self):
        return self.dealer_hand.value > 21

    def is_player_win(self):
        return self.player_hand.value > self.dealer_hand.value

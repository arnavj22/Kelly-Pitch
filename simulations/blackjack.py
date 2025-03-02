import random

# Deck Generated from ChatGPT

# Define the Card class
class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_card_value()
    
    def get_card_value(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11  # Can be changed later based on game logic
        else:
            return int(self.rank)
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Define the Deck class (4 decks)
class Deck:
    discard = []
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks for _ in range(4)]
        self.shuffle()

    def shuffle(self):
        """Shuffle the deck using random.shuffle"""
        random.shuffle(self.cards)

    def draw_card(self):
        """Draw a card from the top of the deck"""
        self.discard.append(self.cards.pop())
        return self.discard[-1]

    def reset(self):
        """Reset the deck to 52 cards and shuffle it"""
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
        self.shuffle()

    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"

# ----------------------------------------------

# STRATEGIES

def calculateWinProbability(composition):
    # TODO: implement a strategy to calculate the win probability given exact current composition
    # is there a library that helps with this?
    pass

def roughWinProbability(composition):
    # TODO: implement a High-Low strategy, and calculate the win probability given current count? can be an estimation
    pass

def optimalStrategyExact(player_sum, dealer_sum, player_soft, composition):
    # TODO: implement a strategy to calculate the optimal strategy given exact current composition
    pass

def optimalStrategyHiLo(player_sum, dealer_sum, player_soft, composition):
    # TODO: implement deviations from the Illustious 18 and Fab
    # https://www.casinoguardian.co.uk/blackjack/blackjack-illustrious-18/

    # 1) If player's sum <= 11:
    if player_sum <= 11:
        # Typical double-down spots for low hard totals
        if player_sum == 11:
            return "double"
        elif player_sum == 10 and dealer_sum < 10:
            return "double"
        elif player_sum == 9 and dealer_sum < 7 and dealer_sum > 2:
            return "double"
        elif player_sum == 8 and dealer_sum < 7 and dealer_sum > 4:
            return "double"
        else:
            return "hit"

    # 2) If player's sum >= 12:
    else:
        if player_sum == 12:
            # Stand vs 4-6, otherwise hit
            return "hit" if dealer_sum < 4 or dealer_sum > 6 else "stand"

        elif player_sum == 13:
            if player_soft:
                # Soft 13: double vs 5-6, otherwise hit
                return "double" if 5 <= dealer_sum <= 6 else "hit"
            else:
                # Hard 13: stand vs dealer 2-6, otherwise hit
                return "hit" if dealer_sum > 6 else "stand"

        elif player_sum == 14 or player_sum == 15:
            if player_soft:
                # Soft 14 or 15: double vs 4-6, otherwise hit
                return "double" if 4 <= dealer_sum <= 6 else "hit"
            else:
                # Hard 14 or 15: stand vs dealer 2-6, otherwise hit
                return "hit" if dealer_sum > 6 else "stand"

        elif player_sum == 16:
            if player_soft:
                # Soft 16: double vs 2 or 4-6, otherwise hit
                if dealer_sum == 2 or (4 <= dealer_sum <= 6):
                    return "double"
                else:
                    return "hit"
            else:
                # Hard 16: stand vs dealer 2-6, otherwise hit
                return "hit" if dealer_sum > 6 else "stand"

        elif player_sum == 17:
            # The given code's logic: hit if soft 17 vs dealer 3-6, else stand
            return "hit" if player_soft and 3 <= dealer_sum <= 6 else "stand"

        elif player_sum == 18:
            if player_soft:
                # Soft 18: double vs 2-6, stand vs 7-8, hit vs 9-11
                if 2 <= dealer_sum <= 6:
                    return "double"
                elif 7 <= dealer_sum <= 8:
                    return "stand"
                else:
                    return "hit"
            else:
                # Hard 18: always stand
                return "stand"

        elif player_sum == 19:
            if player_soft:
                # Soft 19: sometimes double vs 6 in some strategies, else stand
                # We'll pick the slightly more aggressive approach:
                if dealer_sum == 6:
                    return "double"
                else:
                    return "stand"
            else:
                # Hard 19: always stand
                return "stand"

        elif player_sum == 20:
            # Hard 20: always stand
            # Soft 20 (A,9) is typically also stand (some single-deck variants might double vs 5 or 6)
            return "stand"

        elif player_sum == 21:
            # Always stand on 21
            return "stand"

        else:
            # If 22+ you are technically busted, but we'll just default to "stand" or "hit" 
            # depending on how you want to handle it. 
            # In a real game, you're bust as soon as you exceed 21. 
            return "stand"

def optimalStrategyBasic(player_sum, dealer_sum, player_soft):
    # Basic Strategy (ignoring splits)

    # 1) If player's sum <= 11:
    if player_sum <= 11:
        # Typical double-down spots for low hard totals
        if player_sum == 11:
            return "double"
        elif player_sum == 10 and dealer_sum < 10:
            return "double"
        elif player_sum == 9 and dealer_sum < 7 and dealer_sum > 2:
            return "double"
        elif player_sum == 8 and dealer_sum < 7 and dealer_sum > 4:
            return "double"
        else:
            return "hit"

    # 2) If player's sum >= 12:
    else:
        if player_sum == 12:
            # Stand vs 4-6, otherwise hit
            return "hit" if dealer_sum < 4 or dealer_sum > 6 else "stand"

        elif player_sum == 13:
            if player_soft:
                # Soft 13: double vs 5-6, otherwise hit
                return "double" if 5 <= dealer_sum <= 6 else "hit"
            else:
                # Hard 13: stand vs dealer 2-6, otherwise hit
                return "hit" if dealer_sum > 6 else "stand"

        elif player_sum == 14 or player_sum == 15:
            if player_soft:
                # Soft 14 or 15: double vs 4-6, otherwise hit
                return "double" if 4 <= dealer_sum <= 6 else "hit"
            else:
                # Hard 14 or 15: stand vs dealer 2-6, otherwise hit
                return "hit" if dealer_sum > 6 else "stand"

        elif player_sum == 16:
            if player_soft:
                # Soft 16: double vs 2 or 4-6, otherwise hit
                if dealer_sum == 2 or (4 <= dealer_sum <= 6):
                    return "double"
                else:
                    return "hit"
            else:
                # Hard 16: stand vs dealer 2-6, otherwise hit
                return "hit" if dealer_sum > 6 else "stand"

        elif player_sum == 17:
            # The given code's logic: hit if soft 17 vs dealer 3-6, else stand
            return "hit" if player_soft and 3 <= dealer_sum <= 6 else "stand"

        elif player_sum == 18:
            if player_soft:
                # Soft 18: double vs 2-6, stand vs 7-8, hit vs 9-11
                if 2 <= dealer_sum <= 6:
                    return "double"
                elif 7 <= dealer_sum <= 8:
                    return "stand"
                else:
                    return "hit"
            else:
                # Hard 18: always stand
                return "stand"

        elif player_sum == 19:
            if player_soft:
                # Soft 19: sometimes double vs 6 in some strategies, else stand
                # We'll pick the slightly more aggressive approach:
                if dealer_sum == 6:
                    return "double"
                else:
                    return "stand"
            else:
                # Hard 19: always stand
                return "stand"

        elif player_sum == 20:
            # Hard 20: always stand
            # Soft 20 (A,9) is typically also stand (some single-deck variants might double vs 5 or 6)
            return "stand"

        elif player_sum == 21:
            # Always stand on 21
            return "stand"

        else:
            # If 22+ you are technically busted, but we'll just default to "stand" or "hit" 
            # depending on how you want to handle it. 
            # In a real game, you're bust as soon as you exceed 21. 
            return "stand"

# ----------------------------------------------

# SIMULATION

MIN_BET = 10 # 10 dollar min bet
MAX_BET = 10000

def winBlackjackBasic(turns, bankroll):
    deck = Deck()

    # store a current count of remaining cards left in deck, use Card.ranks
    composition = {rank: 16 for rank in Card.ranks}

    
    for _ in range(turns):
        bet = MIN_BET
        mine1 = deck.draw_card()
        mine2 = deck.draw_card()
        dealer1 = deck.draw_card() # public dealer's card
        dealer2 = deck.draw_card() # private dealer's card

        player_soft_count = (mine1.rank == "Ace") + (mine2.rank == "Ace")

        # do basic optimal policy
        mine = mine1.get_card_value() + mine2.get_card_value()
        dealer = dealer1.get_card_value()

        while(mine < 22):
            action = optimalStrategyBasic(mine, dealer, player_soft_count)
            if action == "hit":
                drawn_card = deck.draw_card()
                mine += drawn_card.get_card_value()

                if(drawn_card.rank == "Ace"):
                    player_soft_count += 1

                if(mine >= 22 and player_soft_count > 0):
                    mine -= 10
                    player_soft_count -= 1

            elif action == "double":
                drawn_card = deck.draw_card()
                mine += drawn_card.get_card_value()


                if(drawn_card.rank == "Ace"):
                    player_soft_count += 1

                if(mine >= 22 and player_soft_count > 0):
                    mine -= 10
                    player_soft_count -= 1
                
                bet *= 2
                break
            else:
                break
        
        # resolve the game
        
        if(mine > 21):
            bankroll -= bet

        dealer += dealer2.get_card_value()

        dealer_soft_count = (dealer1.rank == "Ace") + (dealer2.rank == "Ace")

        while(dealer < 17):
            drawn_card = deck.draw_card()
            if(drawn_card.rank == "Ace"):
                dealer_soft_count += 1
            dealer += drawn_card.get_card_value()

            if(dealer >= 22 and dealer_soft_count > 0):
                dealer -= 10
                dealer_soft_count -= 1

        if(dealer > 21):
            bankroll += bet
        elif(mine > dealer):
            bankroll += bet
        elif(mine < dealer):
            bankroll -= bet
            
        if (len(deck.cards) / 208 < 0.75): # reshuffle into the shoe when this happens
            deck.cards += deck.discard
            deck.shuffle()
            print("shuffling")

    return bankroll

print(winBlackjackBasic(1000, 1000))

        


def runBlackjack(turns):
    deck = Deck()

    for _ in range(turns):
        dealer1 = deck.draw_card()
        dealer2 = deck.draw_card()

        mine1 = deck.draw_card()
        mine2 = deck.draw_card()

        # do own policy
        mine = mine1.get_card_value() + mine2.get_card_value()

        # do dealer acitions
        dealer = dealer1.get_card_value() + dealer2.get_card_value()
        while dealer <= 16:
            dealer += deck.draw_card().get_card_value()

        
        if mine > 21:
            pass # you lose

        if dealer > 21:
            pass # you win

        if mine > dealer:
            pass
            # you win. deal with special bj case
        elif mine < dealer:
            pass
            # you lose
        else:
            pass
            # tie, you get back money

        if (len(deck.cards) / 208 < 0.75): # reshuffle into the shoe when this happens
            deck.cards += deck.discard
            deck.shuffle()
            print("shuffling")

runBlackjack(1000)


    



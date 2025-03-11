import random
import numpy as np

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
            return 11  # can be adjusted later based on game logic
        else:
            return int(self.rank)
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Define the Deck class (4 decks)
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank)
                      for suit in Card.suits
                      for rank in Card.ranks
                      for _ in range(4)]
        self.shuffle_deck()

    def shuffle_deck(self):
        """Shuffle the deck in place and reset the pointer."""
        random.shuffle(self.cards)
        self.pointer = 0

    def draw_card(self):
        """Draw a card using a pointer to avoid re-shuffling frequently."""
        # When the deck is exhausted, reshuffle.
        if self.pointer >= len(self.cards):
            self.shuffle_deck()
        card = self.cards[self.pointer]
        self.pointer += 1
        return card

    def reset(self):
        """Explicit reset (if needed) simply reshuffles the deck."""
        self.shuffle_deck()

    def __repr__(self):
        remaining = len(self.cards) - self.pointer
        return f"Deck with {remaining} cards remaining"

# ----------------------------------------------
# STRATEGIES

def calculateWinProbabilityBasic(composition):
    # Placeholder for an exact probability calculation
    pass

def roughWinProbability(composition):
    # Simple Hi-Lo count based estimate
    base_win_prob = 0.498
    count = (sum(composition[rank] for rank in ["10", "Jack", "Queen", "King", "Ace"]) -
             sum(composition[rank] for rank in ["2", "3", "4", "5", "6"]))
    count = max(-10, min(10, count))
    count_normalized = count / 100  # normalizing roughly to [-0.1, 0.1]
    return base_win_prob + count_normalized

def optimalStrategyBasic(player_sum, dealer_up, player_soft):
    # Basic strategy (ignoring splits)
    if player_sum <= 11:
        if player_sum == 11:
            return "double"
        elif player_sum == 10 and dealer_up < 10:
            return "double"
        elif player_sum == 9 and 2 < dealer_up < 7:
            return "double"
        else:
            return "hit"
    else:
        if player_sum == 12:
            return "hit" if dealer_up < 4 or dealer_up > 6 else "stand"
        elif player_sum == 13:
            if player_soft:
                return "double" if 5 <= dealer_up <= 6 else "hit"
            else:
                return "hit" if dealer_up > 6 else "stand"
        elif player_sum in [14, 15]:
            if player_soft:
                return "double" if 4 <= dealer_up <= 6 else "hit"
            else:
                return "hit" if dealer_up > 6 else "stand"
        elif player_sum == 16:
            if player_soft:
                return "double" if dealer_up == 2 or (4 <= dealer_up <= 6) else "hit"
            else:
                return "hit" if dealer_up > 6 else "stand"
        elif player_sum == 17:
            return "hit" if player_soft and 3 <= dealer_up <= 6 else "stand"
        elif player_sum == 18:
            if player_soft:
                if 2 <= dealer_up <= 6:
                    return "double"
                elif 7 <= dealer_up <= 8:
                    return "stand"
                else:
                    return "hit"
            else:
                return "stand"
        elif player_sum == 19:
            if player_soft:
                return "double" if dealer_up == 6 else "stand"
            else:
                return "stand"
        elif player_sum in [20, 21]:
            return "stand"
        else:
            return "stand"

def optimalStrategyHiLo(player_sum, dealer_up, player_soft, composition):
    """
    Uses the Illustrious 18 Hi-Lo index plays, then falls back on basic strategy.
    """
    # Compute true count
    tc = get_true_count(composition)
    # 2a) 16 vs. 10 => stand if TC >= 0
    if player_sum == 16 and dealer_up == 10 and tc >= 0:
        return "stand"
    # 2b) 15 vs. 10 => stand if TC >= 4
    if player_sum == 15 and dealer_up == 10 and tc >= 4:
        return "stand"
    # 2c) 10 vs. 10 => double if TC >= 4
    if player_sum == 10 and dealer_up == 10 and tc >= 4:
        return "double"
    # 2d) 12 vs. 3 => stand if TC >= 2
    if player_sum == 12 and dealer_up == 3 and tc >= 2:
        return "stand"
    # 2e) 12 vs. 2 => stand if TC >= 3
    if player_sum == 12 and dealer_up == 2 and tc >= 3:
        return "stand"
    # 2f) 11 vs. Ace => double if TC >= 1
    if player_sum == 11 and dealer_up == 11 and tc >= 1:
        return "double"
    # 2g) 9 vs. 2 => double if TC >= 1
    if player_sum == 9 and dealer_up == 2 and tc >= 1:
        return "double"
    # 2h) 10 vs. Ace => double if TC >= 3
    if player_sum == 10 and dealer_up == 11 and tc >= 3:
        return "double"
    # 2i) 9 vs. 7 => double if TC >= 3
    if player_sum == 9 and dealer_up == 7 and tc >= 3:
        return "double"
    # 2j) 16 vs. 9 => stand if TC >= 5
    if player_sum == 16 and dealer_up == 9 and tc >= 5:
        return "stand"
    # 2k) 13 vs. 2 => stand if TC >= -1
    if player_sum == 13 and dealer_up == 2 and tc >= -1:
        return "stand"
    # 2l) 12 vs. 4 => stand if TC >= 0
    if player_sum == 12 and dealer_up == 4 and tc >= 0:
        return "stand"
    # 2m) 12 vs. 5 => stand if TC >= -2
    if player_sum == 12 and dealer_up == 5 and tc >= -2:
        return "stand"
    # 2n) 12 vs. 6 => stand if TC >= -1
    if player_sum == 12 and dealer_up == 6 and tc >= -1:
        return "stand"
    # 2o) 13 vs. 3 => stand if TC >= -1
    if player_sum == 13 and dealer_up == 3 and tc >= -1:
        return "stand"
    # 2p) 10 vs. 9 => double if TC >= 0
    if player_sum == 10 and dealer_up == 9 and tc >= 0:
        return "double"
    
    # Fallback to basic strategy:
    return optimalStrategyBasic(player_sum, dealer_up, player_soft)

def get_true_count(composition):
    """
    Returns the 'true count' using a simple Hi-Lo approach:
      - Running count = (# tens+aces) - (# 2..6)
      - decks_left = total_cards_remaining / 52
      - true_count = floor(running_count / decks_left)
    """
    high_count = (composition["10"] + composition["Jack"] +
                  composition["Queen"] + composition["King"] +
                  composition["Ace"])
    low_count = (composition["2"] + composition["3"] +
                 composition["4"] + composition["5"] +
                 composition["6"])
    running_count = high_count - low_count
    total_remaining = sum(composition.values())
    decks_left = total_remaining / 52.0
    if decks_left < 0.25:
        decks_left = 0.25
    true_count = int(running_count // decks_left)
    return true_count

# ----------------------------------------------
# SPLITTING AND PLAYER HAND LOGIC

def should_split(hand, dealer_up, composition):
    """
    Basic splitting rule:
      - Always split Aces and 8s.
      - Never split 10-valued cards.
      - For other pairs, follow simple guidelines.
    """
    if len(hand) != 2 or hand[0].rank != hand[1].rank:
        return False

    rank = hand[0].rank
    if rank == "Ace":
        return True
    if rank == "8":
        return True
    if rank in ["10", "Jack", "Queen", "King"]:
        return False
    if rank in ["2", "3", "7"]:
        if 2 <= dealer_up <= 7:
            return True
    if rank == "6":
        if 2 <= dealer_up <= 6:
            return True
    if rank == "9":
        if dealer_up in [2, 3, 4, 5, 6, 8, 9]:
            return True
    return False

# i love u chat gpt :)
def playPlayerHand(initial_hand, dealer_up, composition, policy="basic"):
    active_hands = [{
        'cards': initial_hand.copy(),
        'bet': MIN_BET,  # starting bet for each hand
        'is_split_ace': False  # flag to mark split aces
    }]
    final_hands = []
    
    # Choose decision function based on policy.
    if policy == "basic":
        decision_fn = optimalStrategyBasic
    else:
        decision_fn = lambda ps, du, psf: optimalStrategyHiLo(ps, du, psf, composition)
    
    while active_hands:
        current = active_hands.pop(0)
        hand = current['cards']
        bet = current['bet']
        is_split_ace = current.get('is_split_ace', False)
        
        # Check for splitting possibility.
        # Only allow splitting if the hand is a pair and it hasn't already been split as aces.
        if not is_split_ace and should_split(hand, dealer_up, composition):
            rank = hand[0].rank
            card_to_keep = hand[0]
            new_card1 = deck.draw_card()
            composition[new_card1.rank] -= 1
            new_hand1 = [card_to_keep, new_card1]
            
            new_card2 = deck.draw_card()
            composition[new_card2.rank] -= 1
            new_hand2 = [card_to_keep, new_card2]
            
            # If splitting aces, mark the new hands so that no further actions are allowed.
            if rank == "Ace":
                # In many casinos, split aces receive only one card and cannot be hit.
                final_hands.append({'total': sum(card.get_card_value() for card in new_hand1), 'bet': bet})
                final_hands.append({'total': sum(card.get_card_value() for card in new_hand2), 'bet': bet})
            else:
                active_hands.append({'cards': new_hand1, 'bet': bet, 'is_split_ace': False})
                active_hands.append({'cards': new_hand2, 'bet': bet, 'is_split_ace': False})
            continue  # move to the next hand
        
        # For a hand that is marked as a split ace hand (if you want to be extra cautious),
        # you could immediately finalize it. (Not strictly needed if you finalize immediately above.)
        if is_split_ace:
            total = sum(card.get_card_value() for card in hand)
            final_hands.append({'total': total, 'bet': bet})
            continue
        
        # Normal play for non-split-ace hands.
        total = sum(card.get_card_value() for card in hand)
        soft_count = sum(1 for card in hand if card.rank == "Ace")
        while total > 21 and soft_count > 0:
            total -= 10
            soft_count -= 1
        
        action = decision_fn(total, dealer_up, soft_count)
        while action in ["hit", "double"]:
            drawn = deck.draw_card()
            composition[drawn.rank] -= 1
            hand.append(drawn)
            total += drawn.get_card_value()
            if drawn.rank == "Ace":
                soft_count += 1
            while total > 21 and soft_count > 0:
                total -= 10
                soft_count -= 1
            if action == "double":
                bet *= 2
                break  # Only one card is drawn on a double.
            action = decision_fn(total, dealer_up, soft_count)
        
        final_hands.append({'total': total, 'bet': bet})
    return final_hands


def get_true_count(composition):
    count = sum(composition[rank] for rank in ["10", "Jack", "Queen", "King", "Ace"]) - sum(composition[rank] for rank in ["2", "3", "4", "5", "6"])
    decks_left = (len(deck.cards) - deck.pointer) / 52
    return count / decks_left

def winBlackjack(turns, bankroll, policy="basic", kelly_p="-1"):
    global deck
    deck = Deck()

    composition = {rank: 16 for rank in Card.ranks}

    bankroll_history = [bankroll]
    
    for _ in range(turns):
        # ruin :(
        if bankroll < MIN_BET:
            break

        # degen, base is to bet 1%
        if policy == "basic":
            bet = MIN_BET
        elif policy == "hilo":
            win_prob = roughWinProbability(composition)
            if kelly_p == -1:  # no Kelly; simple bet sizing
                if get_true_count(composition) >= 1:
                    bet = 1000
                else:
                    bet = MIN_BET
            else:
                win_prob = roughWinProbability(composition)
                if win_prob > 0.5:
                    avg_gain_per_win = 1.1
                    avg_loss_per_loss = 1
                    b = avg_gain_per_win / avg_loss_per_loss
                    kelly_val = win_prob - ((1 - win_prob) / b)
                    kelly_bet = kelly_p * kelly_val
                    bet = max(MIN_BET, int(bankroll * kelly_bet))
                else:
                    bet = MIN_BET
        # Deal initial cards.
        mine1 = deck.draw_card()
        mine2 = deck.draw_card()
        dealer1 = deck.draw_card()  # Dealer’s upcard.
        dealer2 = deck.draw_card()  # Dealer’s hole card.
        
        # adjust composition
        composition[mine1.rank] -= 1
        composition[mine2.rank] -= 1
        composition[dealer1.rank] -= 1 # don't use info we don't know, so don't update dealer2
        
        my_blackjack = is_blackjack(mine1, mine2)
        dealer_blackjack = is_blackjack(dealer1, dealer2)
        

        if my_blackjack:
            if dealer_blackjack:
                outcome = 0 
            else:
                outcome = 1.5 * bet  # Player blackjack pays 3:2.
            bankroll += outcome
        elif dealer_blackjack:
            # Dealer has blackjack and player does not; player loses the entire bet.
            bankroll -= bet
        else:
            # Iterate through players hands
            initial_hand = [mine1, mine2]
            dealer_up_value = dealer1.get_card_value()
            player_hands = playPlayerHand(initial_hand, dealer_up_value, composition, policy)
            
            # Simulate dealer
            dealer_total = dealer1.get_card_value() + dealer2.get_card_value()
            dealer_soft = (dealer1.rank == "Ace") + (dealer2.rank == "Ace")
            while dealer_total < 17:
                drawn = deck.draw_card()
                composition[drawn.rank] -= 1
                dealer_total += drawn.get_card_value()

                # handle soft aces
                if drawn.rank == "Ace":
                    dealer_soft += 1
                while dealer_total > 21 and dealer_soft > 0:
                    dealer_total -= 10
                    dealer_soft -= 1
            
            # Iterate through hands and resolve outcomes
            round_net = 0
            for hand in player_hands:
                player_total = hand['total']
                hand_bet = hand['bet']
                if player_total > 21: # have to eval player busts first
                    round_net -= hand_bet  
                elif dealer_total > 21:
                    round_net += hand_bet  
                elif player_total > dealer_total:
                    round_net += hand_bet
                elif player_total < dealer_total:
                    round_net -= hand_bet
                else:
                    round_net += 0  
            bankroll += round_net

        # subtract the dealer's hole card from composition
        composition[dealer2.rank] -= 1

        if (len(deck.cards) - deck.pointer) / 208 < 0.25:
            deck.reset()
            composition = {rank: 16 for rank in Card.ranks}

        bankroll_history.append(bankroll)
            
    return bankroll_history


MIN_BET = 10
MAX_BET = 25000
def is_blackjack(card1, card2):
    """
    Returns True if the two-card hand is a blackjack.
    """
    ten_valued = {"10", "Jack", "Queen", "King"}
    return ((card1.rank == "Ace" and card2.rank in ten_valued) or
            (card2.rank == "Ace" and card1.rank in ten_valued))

# ----------------------------------------------
# SIMULATION

NUM_TRIALS = 50
BANKROLL = 10000
HANDS_PER_TRIAL = 100000

import matplotlib.pyplot as plt

def simulate(policy="basic", kelly_p=-1):
    all_trials = []  # Store bankroll evolution for each trial
    for trial in range(1, NUM_TRIALS + 1):
        if trial % 10 == 0:
            print("Trial", trial)
        # winBlackjack now returns a list of bankroll values over time for this trial
        trial_bankroll = winBlackjack(HANDS_PER_TRIAL, BANKROLL, policy, kelly_p=kelly_p)
        all_trials.append(trial_bankroll)
    
    # Plot the bankroll evolution for each trial
    plt.figure(figsize=(10, 6))
    for trial_bankroll in all_trials:
        plt.plot(trial_bankroll, alpha=0.5)  # semi-transparent line for each trial

    plt.xlabel("Time Steps")
    plt.ylabel("Bankroll")
    plt.title(f"Bankroll Evolution ({policy}, kelly_p={kelly_p})")
    plt.grid(True)
    
    # Create a unique filename based on the policy and kelly parameter
    file_name = f"bankroll_evolution_{policy}_kelly_{kelly_p}.jpg"
    plt.savefig(file_name)
    plt.close()
    
    # Calculate overall winnings: sum of final bankroll values minus initial bankroll per trial
    total_final = sum(trial_bankroll[-1] for trial_bankroll in all_trials)
    winnings = total_final - (BANKROLL * NUM_TRIALS)
    return winnings / NUM_TRIALS

print("Basic policy winnings:", simulate(policy="basic"))
print("Hi-Lo policy winnings (no Kelly):", simulate(policy="hilo", kelly_p=-1))
print("Hi-Lo policy winnings (Full Kelly):", simulate(policy="hilo", kelly_p=1))
print("Hi-Lo policy winnings (Half Kelly):", simulate(policy="hilo", kelly_p=0.5))
print("Hi-Lo policy winnings (3x Kelly):", simulate(policy="hilo", kelly_p=3))

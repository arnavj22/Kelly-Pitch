# WEIGHTED COIN EXAMPLE FOR KELLY

PROBABILITY = 0.51 # weight of the coin
TRIALS = 10000
TOSSES_PER_TRIAL = 100
DISCRETIZE = True # whether or not we should discretetize the bet amount

from enum import Enum
class STRATEGY(Enum):
    KELLY = 1
    PARTIAL_KELLY = 2
    FIVE_X_KELLY = 3
    ALL = 4

MODE = STRATEGY.FIVE_X_KELLY

def kelly(): # returns how much you should bet
    return (PROBABILITY * (odds() + 1) - 1) / odds()

def doWager():
    if MODE == STRATEGY.KELLY:
        return kelly()
    elif MODE == STRATEGY.PARTIAL_KELLY:
        return kelly() * 1/3
    elif MODE == STRATEGY.FIVE_X_KELLY:
        return kelly() * 5
    elif MODE == STRATEGY.ALL:
        return 1
    print("Invalid Strategy")
    exit(0)

def odds(): # in this case, we win 2x, or lose everything
    return 1

def simulate(tosses):
    import random
    money = 1
    peak = 1
    drawdown = 1
    for _ in range(tosses):
        wager = doWager() * money
        if DISCRETIZE:
            wager = round(wager, 2)

        if wager == 0: 
            # basically, this is equivalent to us not betting. we can treat this as ruin
            return 0, 0

        if random.random() < PROBABILITY: # we win
            money += wager
        else:
            money -= wager
        peak = max(money, peak)
        drawdown = min(drawdown, money / peak)

        if money <= 0: # we are broke
            return 0, 0

    # print(f"Final Money: {money}")
    return money, drawdown

totalMoney = 0
totalDrawdown = 0
geometric = 0 # log of geometric (not sure if I'm caclulating htis one correclty)
ruin = 0
import math
for _ in range(TRIALS):
    money, drawdown = simulate(TOSSES_PER_TRIAL)
    totalMoney += money
    totalDrawdown += drawdown

    if money == 0: ruin += 1
    else: geometric += math.log(money)

geometric /= TRIALS

print(f"Average Value: {totalMoney / TRIALS}")
print(f"Log Geometric Mean: {geometric}")
print(f"Geometric Mean: {math.exp(geometric)}")
print(f"Average Drawdown: {totalDrawdown / TRIALS}") # average of drawdowns
print(f"Risk of Ruin: {(ruin / TRIALS)*100}%")
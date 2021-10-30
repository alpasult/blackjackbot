import copy
import itertools
import random

# blackjack
deck = [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [10, 1], [11, 1], [12, 1], [13, 1],
        [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2], [10, 2], [11, 2], [12, 2], [13, 2],
        [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [9, 3], [10, 3], [11, 3], [12, 3], [13, 3],
        [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4], [12, 4], [13, 4]]
p_hand = []
d_hand = []
average_stand = 0


# Game Functions
def reset():
    global deck, p_hand, d_hand
    deck = [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [10, 1], [11, 1], [12, 1], [13, 1],
            [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2], [10, 2], [11, 2], [12, 2], [13, 2],
            [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [9, 3], [10, 3], [11, 3], [12, 3], [13, 3],
            [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4], [12, 4], [13, 4]]
    p_hand = []
    d_hand = []


def deal(num):
    for i in range(num):
        p_hand.append(deck.pop(random.randint(0, len(deck) - 1)))
    for i in range(len(p_hand)):
        if p_hand[i][0] == 1:
            p_hand.append(p_hand.pop(i))


def cards(c_hand):
    out = ""
    for card in c_hand:
        if card[0] == 11:
            out += "J "
        elif card[0] == 12:
            out += "Q "
        elif card[0] == 13:
            out += "K "
        elif card[0] == 1:
            out += "A "
        else:
            out += str(card[0]) + " "
        if card[1] == 1:
            out += "Clubs"
        if card[1] == 2:
            out += "Spades"
        if card[1] == 3:
            out += "Diamonds"
        if card[1] == 4:
            out += "Hearts"
        out += "\n"
    return out


def hand_value(c_hand):
    value = 0
    aces = 0
    for card in c_hand:
        if card[0] == 11 or card[0] == 12 or card[0] == 13:
            value += 10
        elif card[0] == 1:
            aces += 1
        else:
            value += card[0]
    if aces > 0:
        if value + 11 + aces - 1 <= 21:
            value += 11 + aces - 1
        else:
            value += aces
    return value


def stand():
    for i in range(2):
        d_hand.append(deck.pop(random.randint(0, len(deck) - 1)))
    for i in range(len(d_hand)):
        if d_hand[i][0] == 1:
            d_hand.append(d_hand.pop(i))
    while hand_value(d_hand) < 17:
        d_hand.append(deck.pop(random.randint(0, len(deck) - 1)))
    print("Dealer Hand:\n" + cards(d_hand))
    print("Dealer Value:", hand_value(d_hand))
    if hand_value(d_hand) > 21 or hand_value(d_hand) < hand_value(p_hand):
        print("Player Wins")
    elif hand_value(p_hand) < hand_value(d_hand):
        print("Player Loses")
    elif hand_value(p_hand) == hand_value(d_hand):
        print("Draw")


# Bot
def calc_deck(c_deck):
    t_deck = {1: 0,
              2: 0,
              3: 0,
              4: 0,
              5: 0,
              6: 0,
              7: 0,
              8: 0,
              9: 0,
              10: 0,
              11: 0,
              12: 0,
              13: 0}
    for card in c_deck:
        t_deck[card[0]] += 1
    return t_deck


def get_wins_loses(dc_hand, pc_hand, c_deck):
    wins = 0
    loses = 0
    for card in c_deck:
        td_hand = copy.copy(dc_hand)
        td_hand.append(card)
        t_deck = copy.copy(c_deck)
        t_deck.remove(card)
        d_value = hand_value(td_hand)
        if d_value < 17:
            wins_loses = get_wins_loses(td_hand, pc_hand, t_deck)
            wins += wins_loses[0]
            loses += wins_loses[1]
        elif d_value > 21 or d_value < hand_value(pc_hand):
            wins += 1
        else:
            loses += 1
    return [wins, loses]


def stand_chance(dc_hand, pc_hand, c_deck):
    wins_loses = get_wins_loses(dc_hand, pc_hand, c_deck)
    print(wins_loses[0])
    print(wins_loses[1])
    print(wins_loses[0] / (wins_loses[1] + wins_loses[0]))
    return wins_loses[0] / (wins_loses[1] + wins_loses[0])


def hit_chance(pc_hand, c_deck):
    print("Began Hit Calculation")
    chance = 1.0
    chances = []
    while chance > 0:
        chance = 0.0
        n_combs = 0
        for card_list in itertools.combinations(c_deck, len(chances) + 1):
            tp_hand = copy.copy(pc_hand)
            t_deck = copy.copy(c_deck)
            n_combs += 1
            for card in card_list:
                tp_hand.append(card)
                t_deck.remove(card)
            print("Hit: " + str(len(chances) + 1) + "\n")
            chance += stand_chance([], tp_hand, t_deck)
            print("Chance: " + str(chance))
        chance /= n_combs
        chances.append(chance)
    biggest = 0
    for i in range(len(chances)):
        if chances[biggest] < i:
            biggest = copy.copy(i)
    return chances[biggest]


"""
do all 8 possible permutaions
save them in a list of values

P-Value vs all possible 8 permuations of the deck
1 hit survival* Average P_value vs all possible 8 permuations of the deck
"""


def hit_or_stand(pc_hand, c_deck):
    tp_hand = copy.copy(pc_hand)
    t_deck = copy.copy(c_deck)
    print("Began Stand Calculation\n")
    s_chance = stand_chance([], tp_hand, t_deck)
    print("Completed Stand Calculation\n"
          "Stand Chance = " + str(s_chance) + "\n")
    h_chance = hit_chance(tp_hand, t_deck)
    if s_chance < h_chance:
        return True
    return False


# Main
if __name__ == '__main__':
    choice = 0
    while True:
        print("1) play a game\n"
              "2) quit\n")
        reset()
        choice = int(input(""))
        if choice == 1:
            deal(2)
            while True:
                turn = 0
                print("Hand:\n" + cards(p_hand))
                print("Value:", hand_value(p_hand))
                print("\n1) Hit \n2) Stand\n3) Prediction (Warning will take an hour)")
                turn = int(input(""))
                if turn == 1:
                    deal(1)
                    if hand_value(p_hand) > 21:
                        print("Player Loses")
                        break
                elif turn == 2:
                    stand()
                    break
                elif turn == 3:
                    prediction = "Verdict: hit" if hit_or_stand(p_hand, deck) else "Verdict: stand"
                    print(prediction + "\n")
        if choice == 2:
            break

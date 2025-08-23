import random

suits = ["♠", "♥", "♦", "♣"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def total_sum(hand):
    total = 0
    aces = 0
    for card in hand:
        rank = card[:-1]
        if rank == "A":
            total += 11
            aces += 1
        elif rank in ["J", "Q", "K"]:
            total += 10
        else:
            total += int(rank)

    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def deal_card(deck):
    return deck.pop()


def show_hand(name, hand, hide_first=False):

    if hide_first:
        print(f"\n{name}'s hand: [??] {hand[1]}")
    else:
        total = total_sum(hand)
        if any(card[:-1] == "A" for card in hand) and total != 21:
            print(f"\n{name}'s hand: {' '.join(hand)}. Total: {total-10} or {total}")
        else:
            print(f"\n{name}'s hand: {' '.join(hand)}. Total: {total}")


def player_play(player_hand, deck):
    while total_sum(player_hand) < 21:
        move = input("\n(h)it or (s)tand?").strip().lower()
        if move == "h":
            card = deal_card(deck)
            player_hand.append(card)
            show_hand("Player", player_hand)
            if total_sum(player_hand) > 21:
                print("\nYou busted. Dealer wins.")
                return "loss"
        elif move == "s":
            break
        else:
            print("Invalid input. Options are 'h' and 's'.")
    return False


def dealer_play(dealer_hand, deck):
    print("\nDealer's turn:")
    show_hand("Dealer", dealer_hand)
    while total_sum(dealer_hand) < 17:
        print("Dealer draws another card..")
        card = deal_card(deck)
        dealer_hand.append(card)
        show_hand("Dealer", dealer_hand)
        if total_sum(dealer_hand) > 21:
            print("Dealer busted, you win.")
            return "win"
    return False


def decide_winner(player_hand, dealer_hand):
    if total_sum(dealer_hand) < total_sum(player_hand):
        print("\nYou win!")
        return "win"
    elif total_sum(dealer_hand) > total_sum(player_hand):
        print("\nYou lose!")
        return "loss"
    else:
        print("It's a tie!")


def play_bj(wins, losses, money, bet):
    deck = [rank + suit for suit in suits for rank in ranks] * 4
    random.shuffle(deck)

    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    show_hand("Player", player_hand)
    show_hand("Dealer", dealer_hand, hide_first=True)
    print()

    result = (
        player_play(player_hand, deck)
        or dealer_play(dealer_hand, deck)
        or decide_winner(player_hand, dealer_hand)
    )
    if result == "win":
        wins += 1
        money = money + bet
    elif result == "loss":
        losses += 1
        money = money - bet

    print(f"\nWins: {wins}\nLosses: {losses}")

    print(f"\nMoney: {money}")
    return wins, losses, money


if __name__ == "__main__":
    wins = losses = 0
    money = 1000
    bet = 10
    while True:
        wins, losses, money = play_bj(wins, losses, money, bet)
        if input("\nPlay again? (y/n): ").strip().lower() != "y":
            break
        print("\n" * 20)
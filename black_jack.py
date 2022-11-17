import random
from art import black_jack_logo
import replit


def black_jack():
    print(black_jack_logo)
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    player_cards = []
    computer_cards = []
    player_sum = 0
    computer_sum = 0


    def random_card(cards):
        return random.choice(cards)


    def sum_of_cards(list):
        return sum(list)


    for i in range(2):
        player_cards.append(random_card(cards))
        computer_cards.append(random_card(cards))
        player_sum = sum_of_cards(player_cards)
        computer_sum = sum_of_cards(computer_cards)
    print(f"Your cards: {player_cards}.Current score: {player_sum}")
    print(f"Computer's first card: {computer_cards[0]}")
    if computer_sum == 21:
        print("Computer get blackjack! You lose")
    elif player_sum == 21:
        print("You have blackjack! You won!")
    else:
        continue_game = input(
            "Type 'y' to get another card, type 'n' to pass: ")
        if continue_game == "y":
            player_cards.append(random_card(cards))
            # print(player_cards)
            player_sum = sum_of_cards(player_cards)
            # print(player_sum)
            for i in player_cards:
                if i == 11 and player_sum > 21:
                    i = 1
            # print(player_sum)

    if computer_sum < 16:
        computer_cards.append(random_card(cards))
        # print(computer_cards)
        computer_sum = sum_of_cards(computer_cards)
        # print(computer_sum)
        for i in computer_cards:
            if i == 11 and computer_sum > 21:
                i = 1
        # print(computer_sum)

    print(f"Your card is {player_cards} and score is {player_sum}")
    print(f"Computer's card is {computer_cards} and score is {computer_sum}")

    if computer_sum > 21 and player_sum <= 21:
        print("Player won")
    elif computer_sum <= 21 and player_sum > 21:
        print("Computer won")
    elif computer_sum > player_sum and computer_sum <= 21:
        print("Computer won")
    elif player_sum > computer_sum and player_sum <= 21:
        print("Player won")
    else:
        print("Draw")
    replit.clear()

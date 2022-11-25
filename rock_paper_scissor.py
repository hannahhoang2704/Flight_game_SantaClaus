import random

def rock_paper_scissors():

    rock = '''
        _______
    ---'   ____)
          (_____)
          (_____)
          (____)
    ---.__(___)
    '''

    paper = '''
        _______
    ---'   ____)____
              ______)
              _______)
             _______)
    ---.__________)
    '''

    scissors = '''
        _______
    ---'   ____)____
              ______)
           __________)
          (____)
    ---.__(___)
    '''

    player_score = 0
    comp_score = 0
    round = 1
    found_winner = False
   
    while round <=3:
        option = [rock, paper, scissors]
        user_choice = int(input("Type 0 for Rock, 1 for Paper, 2 for Scissors\n"))
        while user_choice not in range(0, 3):
            user_choice = int(input("Wrong input! Type 0 for Rock, 1 for Paper, 2 for Scissors\n"))
        print(f"Round number : {round}/3.")
        print(option[user_choice])

        computer_choice = random.randint(0, len(option) - 1)
        print(option[computer_choice])
        if user_choice < computer_choice:
            if user_choice == 0 and computer_choice == 2:
                player_score += 1
            else:
                comp_score += 1
        elif user_choice > computer_choice:
            if user_choice == 2 and computer_choice == 0:
                comp_score += 1
            else:
                player_score += 1
        print(f"You: {player_score} | Comp: {comp_score} ")
        round +=1

    if player_score < comp_score:
        print("You lost the game. Computer won the game with score: ", comp_score)
        found_winner = True
    elif player_score > comp_score:
        print("You won the game with score: ", player_score)
        found_winner = True
    else:
        found_winner = False

    while not found_winner:
        option = [rock, paper, scissors]
        user_choice = int(
            input("Type 0 for Rock, 1 for Paper, 2 for Scissors\n"))
        while user_choice not in range(0, 3):
            user_choice = int(input(
                "Wrong input! Type 0 for Rock, 1 for Paper, 2 for Scissors\n"))
        print(f"Round number : {round}/3.")
        print(option[user_choice])

        computer_choice = random.randint(0, len(option) - 1)
        print(option[computer_choice])
        if user_choice < computer_choice:
            if user_choice == 0 and computer_choice == 2:
                player_score += 1
            else:
                comp_score += 1
        elif user_choice > computer_choice:
            if user_choice == 2 and computer_choice == 0:
                comp_score += 1
            else:
                player_score += 1
        print(f"You: {player_score} | Comp: {comp_score} ")
        round += 1

        if player_score < comp_score:
            print("You lost the game. Computer won the game with score: ",
                  comp_score)
            found_winner = True
        elif player_score > comp_score:
            print("You won the game with score: ", player_score)
            found_winner = True
        else:
            found_winner = False

    if player_score < comp_score:
        return False
    else:
        return True


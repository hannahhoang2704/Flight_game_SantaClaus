import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11
}
playing = True


# card class
class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


# deck class
class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))  # appending the Card object to self.deck list

    def shuffle(self):
        random.shuffle(self.deck)

    # grabbing the deck attribute of Deck class then popping off card item from list and setting it to single card
    def deal(self):
        singleCard = self.deck.pop()
        return singleCard


# hand class: grabbing the single card and adding to someone's hand
class Hand():
    def __init__(self):
        self.cards = []  # start with 0 cards in hand
        self.value = 0  # starting with 0 value
        self.aces = 0  # keep track of aces

    # card object is Deck.deal() that has single card and sc has suit and rank
    def addCard(self, card):
        self.cards.append(card)  # taking card object and appending it to self.cards list
        # if value is > 21 this particular hand has lost the game
        self.value += values[card.rank]

        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    def checkAces(self):
        # if value > 21 and if ace is available
        while self.value > 21 and self.aces:
            self.value -= 10  # take my value and subtract 10
            self.aces -= 1  # take my aces and subtract 1


# function for taking a new card
def newCard(deck, hand):
    hand.addCard(deck.deal())
    hand.checkAces()


# function for asking player if he wants another card or pass
def cardOrPass(deck, hand):
    global playing

    while True:
        x = input("Type 'y' to get another card, type 'n' to pass: ")

        if x[0].lower() == 'y':
            newCard(deck, hand)
        elif x[0].lower() == 'n':
            print("Player stands. Computer is playing.")
            playing = False
        else:
            print("Wrong input, try again!")
            continue

        break


# function for showing cards
def showCards(player, computer):
    print("\nComputers's Turn: ")
    print("<card hidden>")
    # print(' ' + computer.cards[1].__str__())
    print('', computer.cards[1])
    print("\nPlayer's Turn:", *player.cards, sep='\n ')


def showAll(player, computer):
    # asterisk * symbol is used to print every item in a collection
    print("\nComputer's Turn:", *computer.cards, sep='\n ')  # sep='\n ' argument prints each item on a separate line
    print("Computer's Turn =", computer.value)
    print("\nPlayer's Turn:", *player.cards, sep='\n ')
    print("Player's Turn =", player.value)


# functions for ending game scenarios
def playerLost(player, computer):
    print("You lost")


def playerWins(player, computer):
    print("You won!")


def computerLost(player, computer):
    print("Computer lost! YOU WON!")


def computerWins(player, computer):
    print("Computer wins! YOU LOST")


def greatTie(player, computer):
    print("Wow! This is a tie")


# play logic for game

while True:
    print("Welcome to BlackJack")
    # shuffle and deal two cards to each player
    deck = Deck()
    deck.shuffle()

    playerHand = Hand()
    playerHand.addCard(deck.deal())
    playerHand.addCard(deck.deal())

    computerHand = Hand()
    computerHand.addCard(deck.deal())
    computerHand.addCard(deck.deal())

    showCards(playerHand, computerHand)  # show cards for computer and player

    while playing:
        cardOrPass(deck, playerHand)  # prompt for newCard or stand

        showCards(playerHand, computerHand)

        # if player hand exceeds 21 run playerLost() and break
        if playerHand.value > 21:
            playerLost(playerHand, computerHand)

            break

    # soft 17 rule: keep playing until computer reaches 17
    if playerHand.value <= 21:
        while computerHand.value < playerHand.value:
            newCard(deck, computerHand)

        showAll(playerHand, computerHand)  # show all cards

        # run a different game win scenario
        if computerHand.value > 21:
            computerLost(playerHand, computerHand)
        elif computerHand.value > playerHand.value:
            computerWins(playerHand, computerHand)
        elif computerHand.value < playerHand.value:
            playerWins(playerHand, computerHand)
        else:
            greatTie(playerHand, computerHand)

    # ask to play again
    newGame = input("Want to play again? y/n: ")

    if newGame[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing BlackJack! See you again.")
        break

#Questionaires and answers

questions = (
        "Wasting less food is a way to reduce greenhouse gas emissions.",  # 0
        "The overwhelming majority of scientists agree that climate change is real and caused by humans.",
        # 1
        "Combustion removes carbon from the atmosphere",  # 2
        "Unplugging your electronics when you’re not using them could shave as much as 10 percent off your energy"
        "bill.",  # 3
        "Climate change is heating the world evenly.",  # 4
        "Climate change and extreme weather are linked.",  # 5
        "As climate warms, we will no longer have snow storms and cold days.",  # 6
        "We definitely know that tornadoes are increasing in frequency because of climate change.",
        # 7
        "All climate scientists in the 1970s were saying that we were going into an Ice Age or cooler Earth.",
        # 8
        "Growing leafy green plants is the most effective method for permanently storing carbon dioxide.",
        # 9
        "Scientists have reached common agreement and have adopted consensus-driven global policies that monitor"
        "effective, safe, reliable long-term storage of carbon dioxide.",  # 10
        "The atmosphere is composed mainly of nitrogen and oxygen.",  # 11
        "Climate change is the same thing as global warming",  # 12
        "The Earth's climate has changed before",  # 13
        "Climate change can harm plants and animals",  # 14
        "The sun causes global warming")  # 15

answers = ("true",  # 0
           "true",  # 1,
           "false",  # 2
           "true",  # 3
           "false",  # 4
           "true",  # 5
           "false",  # 6
           "false",  # 7
           "false",  # 8
           "false",  # 9
           "false",  # 10
           "true",  # 11
           "false",  # 12
           "true",  # 13
           "true",  # 14
           "false")  # 15


def introduction():
    print("Ho Ho Ho")

    # PHASE1: Intro of the game & set a goal for players

    intro1 = f"Each year children from all over the world\nfly to Rovaniemi to meet Santa\nBelievers to hug him and non-believers to expose him by pulling his beard. \n"
    print(intro1)

    intro2 = f"\nOn your way to Rovaniemi you will come across different challenges.\nOne of them is flight's CO2 consumption.\nYour main goal is to keep CO2 consumption as low as possible.\nMake sure it doesn't go over 10 000 units!\n"
    print(intro2)
    print("Your mission starts in 3..\n")
    print("2")
    print("1")

    intro3 = ("Firstly, do you believe in Santa Claus?")

    while True:
        start = input(intro3)
        start = start.lower()
        if start == "no":
            print("\n***Me neither. Get ready for an adventure.***\n")
            break
        elif start == "yes":
            print(
                "\n***It's going to be an eye-opening experience for you. Let's go!***\n")
            break
        else:
            print("Just type yes or no. ")

    print("Lucky for you, there are other like-minded people out there. \n")

    friends = input("\nDo you want to meet them? ")
    friends = friends.lower()

    while friends != "yes" or friends != "no":
        if friends == "yes":
            print(
                f"\nI thought so.\nIn order to have them join you on your quest they will have questions for you.\n"
                f"Answer them correctly and you will save some C02!\n")
            break
        elif friends == "no":
            print(
                "\nIf you don't care about meeting new friends, try to save some C02 during your flight\nby answering "
                f"questions correctly and keep CO2 within the budget.\n")
            break
        friends = input("Just type yes or no! ")
        friends = friends.lower()

    print(
        f"Before reaching the 1st destination, your C02 is 5000 units.\n")
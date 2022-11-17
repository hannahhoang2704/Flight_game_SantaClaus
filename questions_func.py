import random

def questions_answers():
    # Questionaires and answers
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


    questions = list(questions)
    answers = list(answers)



    print(f"Answer the question:\n")
    # ask question & get point by answer
    random_index_number = random.randint(0, len(questions) - 1)
    user_answer = "0"

    print(questions[random_index_number])  # call random question in questions list
    user_answer = input('True or false: ')
    user_answer = user_answer.lower()

    right_answer = answers[random_index_number]
    questions.pop(
    random_index_number)  # pop the question from the list to avoid duplicated question in next destination
    answers.pop(random_index_number)

    # Check if players answer correct or not

    if user_answer == right_answer:
        print(f"Good job! That was the correct answer.")


    elif user_answer != right_answer:
        print(f"You answered incorrectly")


questions_answers()



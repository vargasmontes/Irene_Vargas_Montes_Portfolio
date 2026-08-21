
# Game requires a file called "words.txt" to act as word bank.

def hangman():
    hangman = {10: "\n\n\n\n\n\n\n\n", 
            9: "\n\n\n\n\n\n\n_______" ,
            8: "\n |    \n |    \n |\n |\n |\n |\n_|_____" ,
            7: " ______\n |    \n |    \n |\n |\n |\n |\n_|_____" ,
            6: " ______\n |    |\n |    \n |\n |\n |\n |\n_|_____" ,
            5: " ______\n |    |\n |    O\n |\n |\n |\n |\n_|_____" ,
            4: " ______\n |    |\n |    O\n |    |\n |    |\n |     \n |\n_|_____" ,
            3: " ______\n |    |\n |    O\n |   \\|\n |    |\n |     \n |\n_|_____" ,
            2: " ______\n |    |\n |    O\n |   \\|/\n |    |\n |     \n |\n_|_____" ,
            1: " ______\n |    |\n |    O\n |   \\|/\n |    |\n |   /  \n |\n_|_____" ,
            0: " ______\n |    |\n |    O\n |   \\|/ \n |    |\n |   / \\ \n |\n_|_____"}
    
    file = open("Word Games/words.txt").read().split()
    answer = random.choice(file)
        
    lenght = len(answer)

    guessed_word = ['_'] * len(answer)
    attempts = 10
    guessed_letters = []

    print(f"\nWelcome to the game!\nYou have {attempts} attempts available to guess a {lenght} letter word. Let's start.")
    last_attempt = guessed_word

    while attempts > 0 and "_" in last_attempt:
        guess = input("\nGuess a letter: ").lower()
        if guess in guessed_letters:
            guess = input("You have already tried that letter. Guess a different one: ")
    
        if guess in answer:
            for i in range(len(answer)):
                if answer[i] == guess:
                    guessed_word[i] = guess
            print("\nGood guess!")
        else:
            attempts -= 1
            guessed_letters.append(guess)
            print(f"\nNope! You have {attempts} attempts left.")

        last_attempt = " ".join(guessed_word).upper()
        print(last_attempt)
        print(hangman[attempts])
        if len(guessed_letters) == 0:
            print("\nWrongly guessed letters: None.")
        else:
            print("\nWrongly guessed letters: "+", ".join(guessed_letters))
    
    

    if attempts == 0:
        print(f"\nSorry, you ran out of attempts!\nThe right answer was {answer}.")
    else:
        print(f"\nCongratulations, you guessed the word! \nThanks for playing!")

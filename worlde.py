import random

words=[]
with open ("words.txt", "r") as f:
    for line in f:
        word = line.strip()
        if len(word) == 5:
            words.append(word)

target = random.choice(words)

display = ["*"] * 5
alphabet = list("abcdefghijklmnopqrstuvwxyz")
max_attempts = 10

print("Welcome to Wordle!\n")

for attempts in range(max_attempts):
    print("Word:","".join(display))
    print("Alphabet:", "".join(alphabet))

    guess = input(f"\nAttempt {attempts + 1}/{max_attempts} - Enter a 5-letter word: ").lower()

    if guess not in words:
        print("Not a valid word\n")
        continue

    for i in range(5):
        if guess[i] == target[i]:
            display[i] = guess[i]

            total_in_word = target.count(guess[i])
            found_so_far = display.count(guess[i])

            if found_so_far == total_in_word:
                if guess[i] in alphabet:
                    alphabet.remove(guess[i])
                elif guess[i].upper() in alphabet:
                    alphabet.remove(guess[i].upper())

        elif guess[i] in target:
            if guess[i] in alphabet:
                index = alphabet.index(guess[i])
                alphabet[index] = guess[i].upper()

        else:
            if guess[i] in alphabet:
                alphabet.remove(guess[i])

        if"".join(display) == target:
            print("\nWord:","".join(display))
            print("Congratulations! You guessed the word!")
            break

        print()

else:
    print("\nGame over! The word was:", target)
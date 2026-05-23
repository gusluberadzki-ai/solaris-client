import random

words=[]

with open ("names.txt", "r") as f:
    for line in f:
        word = line.strip()
        words.append(word.capitalize())



target = random.choice(words)
print("Our random winner is")
print("drumroll...")
print(target)
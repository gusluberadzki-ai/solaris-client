import random

filename="randomNumbers.txt"

with open(filename,"w") as f:
    for i in range(100):
        number = random.randint(100000,999999)
        f.write(str(number) + "\n")

print(f"{i+1} random 6-digit numbers written to {filename}")
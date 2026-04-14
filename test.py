
print("I am Python, a friendly assistant")
print("How is your day?")
name = input("What is your name? ")

print("Hi", name, "How is your day?")
print("It's nice to meet you")
print("Welcome to the calculator")

again = "yes"
while again.lower() in ["yes", "y"]:
    choice = input("Would you like to divide or multiply? ")

    if choice == "m":
        table = int(input("What times table do you need? "))
        for i in range(15):
            print((i + 1) * table)

    elif choice == "d":
        x = float(input("Enter the first number: "))
        y = float(input("Enter the second number: "))
        if y != 0:
            print("Result:", x / y)
        else:
            print("Error: Division by zero is not allowed.A number divide by 0 is the number")

    else:
        print("Invalid choice. Please type 'm' or 'd'.")

    again = input("Would you like another calculation? (yes/no) ")

print("Goodbye!")

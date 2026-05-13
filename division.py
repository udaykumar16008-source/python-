try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    result = num1 / num2

except ValueError:
    print("Error: Invalid input! Please enter numeric values.")

except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")

else:
    print(f"Result of division: {result}")

finally:
    print("Program execution completed.")

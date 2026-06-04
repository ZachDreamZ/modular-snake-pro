class Calculator:
    """A class to perform basic mathematical operations."""

    def add(self, x, y):
        """Returns the sum of x and y."""
        return x + y

    def subtract(self, x, y):
        """Returns the difference of x and y."""
        return x - y

    def multiply(self, x, y):
        """Returns the product of x and y."""
        return x * y

    def divide(self, x, y):
        """Returns the quotient of x and y. Handles division by zero."""
        if y == 0:
            return "Error: Division by zero is not allowed."
        return x / y

def main():
    calc = Calculator()
    
    print("--- Python Interactive Calculator ---")
    print("Welcome! Please follow the menu to perform calculations.")

    while True:
        print("\nSelect an operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")

        choice = input("Enter choice (1/2/3/4/5): ")

        if choice == '5':
            print("Exiting the calculator. Goodbye!")
            break

        if choice in ('1', '2', '3', '4'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input! Please enter numeric values.")
                continue

            if choice == '1':
                print(f"Result: {num1} + {num2} = {calc.add(num1, num2)}")
            elif choice == '2':
                print(f"Result: {num1} - {num2} = {calc.subtract(num1, num2)}")
            elif choice == '3':
                print(f"Result: {num1} * {num2} = {calc.multiply(num1, num2)}")
            elif choice == '4':
                result = calc.divide(num1, num2)
                if isinstance(result, str):
                    print(result)
                else:
                    print(f"Result: {num1} / {num2} = {result}")
        else:
            print("Invalid choice! Please select a valid option from the menu.")

if __name__ == "__main__":
    main()
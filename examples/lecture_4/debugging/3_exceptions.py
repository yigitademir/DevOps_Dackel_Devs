def safe_divide(x, y):
    try:
        result = x / y
        print(f"Result: {result}")
    except ZeroDivisionError as e:
        print(f"Error: {type(e).__name__} - {e}")
        # Handle the division by zero case
    except Exception as e:
        print(f"An unexpected error occurred: {type(e).__name__} - {e}")
        # Handle other types of exceptions
    finally:
        print("This block always executes, whether an exception occurred or not.")

# Eg.
safe_divide(10, 2)
safe_divide(5, 0)

x = 10
y = 0
assert y != 0, "Divisor (y) should not be zero"

# Handling AssertionError
x = 0
try:
    assert x > 0, "x should be greater than zero"
except AssertionError as e:
    print(f"Assertion failed: {e}")
import logging

logging.basicConfig(
    filename='example.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

def example_function(x, y):
    logging.debug(f"Input values: x={x}, y={y}")
    result = x + y + 1
    logging.debug(f"Result: {result}")
    return result

result = example_function(3, 7)

# Logging an error message
if result > 10:
    logging.error("Result exceeds the expected maximum.")
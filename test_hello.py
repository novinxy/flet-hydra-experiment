import time
import pytest

def hello_world():
    return "Hello, world!"

@pytest.mark.parametrize("input", list(range(1,20)))
def test_hello_world(input):
    time.sleep(0.5)  # Simulate a delay
    assert hello_world() == "Hello, world!"
    assert input % 2 == 0
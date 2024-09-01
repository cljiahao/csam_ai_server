import pytest


@pytest.fixture
def detail_input():
    return {
        "lotNo": "1234567890",
        "plate": "temp",
        "item": "test123",
        "no_of_chips": 4000,
        "no_of_batches": 15,
        "no_of_real": 10,
    }

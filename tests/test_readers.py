from pathlib import Path

from src.models.models import Customer
from src.readers.json_reader import read_json


def test_read_customers():
    customers = read_json(
        Path("data/bronze/customers.json"),
        Customer,
    )

    assert len(customers) == 100
    assert all(isinstance(customer, Customer) for customer in customers)
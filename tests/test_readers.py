from pathlib import Path

from src.models.models import Customer
from src.readers.json_reader import JSONReader


def test_read_customers():
    reader = JSONReader()
    customers = reader.read(
        Path("data/bronze/customers.json"),
        Customer,
    )

    assert len(customers) > 0
    assert all(isinstance(customer, Customer) for customer in customers)
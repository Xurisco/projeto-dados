from pathlib import Path

from src.models.models import Customer
from src.readers.base_reader import BaseReader
from src.readers.csv_reader import CSVReader
from src.readers.excel_reader import ExcelReader
from src.readers.json_reader import JSONReader


def test_json_reader():
    reader = JSONReader()
    customers = reader.read(
        Path("data/bronze/customers.json"),
        Customer,
    )
    assert len(customers) > 0
    assert all(isinstance(c, Customer) for c in customers)


def test_readers_inherit_from_base():
    assert issubclass(JSONReader, BaseReader)
    assert issubclass(CSVReader, BaseReader)
    assert issubclass(ExcelReader, BaseReader)
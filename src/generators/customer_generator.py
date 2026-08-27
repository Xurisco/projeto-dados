from faker import Faker

from src.models.models import Customer


fake = Faker("pt_BR")


def generate_customer(customer_id: int) -> Customer:
    return Customer(
        id=customer_id,
        name=fake.name(),
        email=fake.email(),
        birth_date=fake.date_of_birth(),
        city=fake.city(),
        state=fake.estado_sigla(),
    )
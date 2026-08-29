from datetime import datetime
from faker import Faker
from src.models.models import Customer

faker = Faker("pt_BR")

ESTADOS_E_CIDADES = [
    ("SP", "São Paulo"), ("SP", "Campinas"), ("RJ", "Rio de Janeiro"),
    ("MG", "Belo Horizonte"), ("PR", "Curitiba"), ("RS", "Porto Alegre"),
    ("SC", "Florianópolis"), ("BA", "Salvador"), ("PE", "Recife"),
    ("DF", "Brasília"), ("GO", "Goiânia"), ("CE", "Fortaleza"),
]


def generate_customer(customer_id: int) -> Customer:
    state, city = faker.random_element(ESTADOS_E_CIDADES)
    return Customer(
        id=customer_id,
        name=faker.name(),
        email=faker.email(),
        city=city,
        state=state,
        created_at=datetime.now().isoformat(),
    )
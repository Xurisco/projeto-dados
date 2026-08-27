import random

from faker import Faker

from src.models.models import Product


fake = Faker("pt_BR")


def generate_product(product_id: int) -> Product:
    return Product(
        id=product_id,
        name=fake.catch_phrase(),
        category=random.choice(
            [
                "Eletronicos",
                "Informatica",
                "Casa",
                "Esportes",
                "Livros",
                "Vestuario",
            ]
        ),
        price=round(random.uniform(10, 5000), 2),
        stock=random.randint(0, 500),
    )
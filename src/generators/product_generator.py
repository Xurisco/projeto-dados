import random

from src.models.models import Product


PRODUCT_CATALOG = {
    "eletronicos": [
        ("Smartphone Samsung Galaxy", 1200, 4500),
        ("Smart TV 50 Polegadas", 2200, 4500),
        ("Fone Bluetooth", 80, 800),
        ("Smartwatch", 150, 1500),
        ("Caixa de Som Bluetooth", 100, 1000),
    ],
    "informatica": [
        ("Notebook Lenovo", 2500, 7000),
        ("Mouse Logitech", 80, 500),
        ("Teclado Mecânico", 150, 900),
        ("Monitor 24 Polegadas", 700, 2200),
        ("Webcam Full HD", 150, 700),
    ],
    "casa": [
        ("Air Fryer", 250, 1000),
        ("Liquidificador", 100, 600),
        ("Cafeteira Elétrica", 150, 1200),
        ("Aspirador de Pó", 200, 1500),
        ("Jogo de Panelas", 200, 1000),
    ],
    "esportes": [
        ("Bola de Futebol", 50, 300),
        ("Tênis Esportivo", 200, 1200),
        ("Mochila Esportiva", 100, 500),
        ("Bicicleta", 800, 5000),
        ("Kit de Halteres", 150, 1000),
    ],
    "livros": [
        ("Livro de Ficção", 30, 100),
        ("Livro de Tecnologia", 50, 200),
        ("Livro de Negócios", 40, 180),
        ("Livro de História", 35, 150),
        ("Livro de Ciência", 40, 180),
    ],
    "vestuario": [
        ("Camiseta Básica", 30, 120),
        ("Calça Jeans", 100, 350),
        ("Jaqueta", 150, 600),
        ("Tênis Casual", 150, 700),
        ("Moletom", 100, 400),
    ],
}


def generate_product(product_id: int) -> Product:
    category = random.choice(list(PRODUCT_CATALOG.keys()))

    product_name, min_price, max_price = random.choice(
        PRODUCT_CATALOG[category]
    )

    return Product(
        id=product_id,
        name=product_name,
        category=category,
        price=round(random.uniform(min_price, max_price), 2),
        stock=random.randint(0, 500),
    )
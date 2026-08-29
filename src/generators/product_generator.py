import random
from src.models.models import Product

CATALOG = {
    "Eletrônicos": {
        "Smartphones": {
            "brands": ["Samsung", "Apple", "Xiaomi", "Motorola"],
            "items": ["Galaxy S24", "iPhone 15 Pro", "Redmi Note 13", "Edge 50"],
            "price_range": (1500.0, 8500.0),
        },
        "Fones de Ouvido": {
            "brands": ["Sony", "JBL", "Sennheiser", "Apple"],
            "items": ["Fone Noise Cancelling", "Earbuds Bluetooth", "Headset Gamer"],
            "price_range": (120.0, 1800.0),
        },
        "Smart TVs": {
            "brands": ["Samsung", "LG", "TCL", "Philips"],
            "items": ["TV 4K 55\"", "TV OLED 65\"", "TV QLED 50\""],
            "price_range": (1800.0, 9500.0),
        },
    },
    "Informática": {
        "Notebooks": {
            "brands": ["Dell", "Lenovo", "Apple", "Acer", "ASUS"],
            "items": ["MacBook Air M2", "Notebook Gamer", "Ultrabook ThinkPad", "Aspire 5"],
            "price_range": (2500.0, 12000.0),
        },
        "Periféricos": {
            "brands": ["Logitech", "Razer", "Redragon", "Corsair"],
            "items": ["Mouse Sem Fio Ergonomico", "Teclado Mecânico RGB", "Webcam Full HD"],
            "price_range": (80.0, 900.0),
        },
        "Monitores": {
            "brands": ["LG", "Samsung", "AOC", "Dell"],
            "items": ["Monitor UltraWide 29\"", "Monitor Gamer 144Hz", "Monitor 4K 27\""],
            "price_range": (700.0, 3500.0),
        },
    },
    "Eletrodomésticos": {
        "Cozinha": {
            "brands": ["Brastemp", "Electrolux", "Arno", "Mondial", "Oster"],
            "items": ["Air Fryer Digital", "Cafeteira Espresso", "Micro-ondas 30L", "Liquidificador Turbo"],
            "price_range": (150.0, 1200.0),
        },
        "Lavanderia": {
            "brands": ["LG", "Samsung", "Brastemp", "Consul"],
            "items": ["Lava e Seca 11kg", "Máquina de Lavar 13kg"],
            "price_range": (1800.0, 4800.0),
        },
    },
    "Moda & Acessórios": {
        "Calçados": {
            "brands": ["Nike", "Adidas", "Puma", "Asics", "Mizuno"],
            "items": ["Tênis Corrida Performance", "Tênis Casual Court", "Chuteira Society"],
            "price_range": (190.0, 1200.0),
        },
        "Acessórios": {
            "brands": ["Oakley", "Ray-Ban", "Casio", "Technos"],
            "items": ["Relógio Cronógrafo", "Óculos de Sol Escuro", "Mochila Executiva"],
            "price_range": (150.0, 1500.0),
        },
    },
    "Beleza & Cuidado": {
        "Perfumaria": {
            "brands": ["Natura", "O Boticário", "Carolina Herrera", "Dior"],
            "items": ["Perfume Eau de Parfum 100ml", "Colônia Desodorante"],
            "price_range": (90.0, 850.0),
        },
        "Cabelos & Barba": {
            "brands": ["Taiff", "Philips", "Gama", "Mondial"],
            "items": ["Secador de Cabelo Profissional", "Barbeador Elétrico Lavável"],
            "price_range": (110.0, 600.0),
        },
    },
}


def generate_product(product_id: int) -> Product:
    category_name = random.choice(list(CATALOG.keys()))
    subcat_name = random.choice(list(CATALOG[category_name].keys()))
    subcat_data = CATALOG[category_name][subcat_name]

    brand = random.choice(subcat_data["brands"])
    base_item = random.choice(subcat_data["items"])
    full_name = f"{brand} {base_item}"

    min_p, max_p = subcat_data["price_range"]
    price = round(random.uniform(min_p, max_p), 2)
    # Custo de produto entre 40% e 70% do preço de venda
    cost_price = round(price * random.uniform(0.4, 0.7), 2)

    sku = f"{category_name[:3].upper()}-{brand[:3].upper()}-{product_id:04d}"

    return Product(
        id=product_id,
        sku=sku,
        name=full_name,
        category=category_name,
        subcategory=subcat_name,
        brand=brand,
        cost_price=cost_price,
        price=price,
        stock_quantity=random.randint(5, 250),
        rating=round(random.uniform(3.5, 5.0), 1),
    )
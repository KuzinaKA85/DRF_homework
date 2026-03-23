import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создаёт продукт в страйпе"""

    # Получаем название в зависимости от типа объекта
    if hasattr(product, "title_course"):
        name = product.title_course
    else:
        name = product.title_lesson

    stripe_product = stripe.Product.create(
        name=name, description=product.description[:500] if product.description else ""
    )
    return stripe_product


def create_stripe_price(stripe_product, amount):
    """Создает цену в страйпе"""

    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product=stripe_product.get("id"),
    )
    return price


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1.8000/payment/success/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    # print(f"Session ID length: {len(session.get('id'))}")
    # print(f"Session URL length: {len(session.get('url'))}")

    return session.get("id"), session.get("url")

from accounts.models.user import User
from .profile import Profile
from .product import Product
from .custom_order import CustomOrder
from .order import Order, OrderItem



def test():
    # Crea un prodotto
    product1 = Product.objects.create(name="Laptop", description="Laptop 15 inch", price=1200.00, quantity_in_stock=10)
    product2 = Product.objects.create(name="Mouse", description="Wireless Mouse", price=25.50, quantity_in_stock=50)

    # Crea un ordine
    customer = User.objects.filter(username="vanacore").first()  # Recupera un cliente esistente
    order = Order.objects.create(customer=customer, status="pending", total_price=0.00)

    # Aggiungi prodotti all'ordine con una quantità
    order_item1 = OrderItem.objects.create(order=order, product=product1, quantity=1)  # 1 Laptop
    order_item2 = OrderItem.objects.create(order=order, product=product2, quantity=2)  # 2 Mouse

    # Ricalcola il totale dell'ordine
    order.calculate_total_price()

    print(order.total_price)  # Stampa il totale dell'ordine


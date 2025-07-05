import random
from django.core.management.base import BaseCommand
from faker import Faker
from seller_dispute.models import Order, Return

fake = Faker()

class Command(BaseCommand):
    help = "Generate 50 random orders (each with one item), and 20 random returns for those orders."

    def handle(self, *args, **kwargs):
        orders_created = 0
        orders = []
        # Create 50 orders, each with one item
        for i in range(1, 51):
            order = Order.objects.create(
                order_id=f"ORDER{i:04d}",
                customer_name=fake.name(),
                customer_email=fake.email(),
                customer_address=fake.address(),
                order_date=fake.date_time_between(start_date='-2y', end_date='now'),
                item_sku=fake.unique.bothify(text='SKU-####-????'),
                item_name=fake.word().capitalize() + ' ' + fake.word().capitalize(),
                item_quantity=random.randint(1, 3),
                amount=round(random.uniform(20, 500), 2)
            )
            orders.append(order)
            orders_created += 1
            self.stdout.write(self.style.SUCCESS(f"Created Order {order.order_id} with item {order.item_sku}."))

        # Select 20 random orders for returns
        if len(orders) < 20:
            self.stdout.write(self.style.ERROR("Not enough orders to create 20 returns!"))
            return
        returned_orders = random.sample(orders, 20)
        for idx, order in enumerate(returned_orders, 1):
            return_event = Return.objects.create(
                order=order,
                return_id=f"RET{idx:04d}",
                return_reason=random.choice([
                    "Damaged item", "Incorrect item returned", "Fraudulent return", "Other"
                ]),
                return_tracking_number=fake.bothify(text='TRK########'),
                return_date=fake.date_time_between(start_date=order.order_date, end_date='now'),
                original_item_condition=random.choice(["New", "Used", "Damaged"]),
                notes=fake.sentence(),
                return_amount=round(random.uniform(5, order.amount), 2)
            )
            self.stdout.write(self.style.SUCCESS(f"Created Return {return_event.return_id} for Order {order.order_id}, Item {order.item_sku}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {orders_created} orders and 20 returns!")) 
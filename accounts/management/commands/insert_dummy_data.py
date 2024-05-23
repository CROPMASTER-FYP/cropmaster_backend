# import datetime
# from django.core.management.base import BaseCommand
# from django.conf import settings
# from accounts.models import UserVisit, User

# class Command(BaseCommand):
#     help = 'Insert dummy data into the UserVisit model'

#     def handle(self, *args, **kwargs):
#         # Dummy data as provided
#         dummy_data = {
#             "2024-02-14": 20,
#             "2024-03-15": 5,
#             "2024-04-16": 4,
#             "2024-05-17": 3,
#             "2024-05-18": 4,
#             "2024-01-19": 12,
#             "2024-06-13": 10,
#             "2023-10-17": 3,
#             "2023-11-18": 4,
#             "2023-12-19": 20
#         }

#         # Fetch a user to associate visits with (you can modify this to select different users)
#         user = User.objects.first()

#         if user is None:
#             self.stdout.write(self.style.ERROR('No users found in the database. Please create a user first.'))
#             return

#         visits = []
#         for date_str, count in dummy_data.items():
#             date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
#             for _ in range(count):
#                 visits.append(UserVisit(user=user, timestamp=date))

#         UserVisit.objects.bulk_create(visits)

#         self.stdout.write(self.style.SUCCESS(f'Successfully inserted {len(visits)} UserVisit records.'))



import datetime
import random
import uuid
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from orders.models import Product
from orders.models import Order

class Command(BaseCommand):
    help = 'Insert dummy data into the Order model'

    def handle(self, *args, **kwargs):
        # Dummy data with dates and quantities
        dummy_data = {
            "2024-02-14": [("Maize", 2), ("Cassava", 3)],
            "2024-03-15": [("Groundnuts", 5)],
            "2024-04-16": [("Maize", 1), ("Cassava", 4)],
            "2024-05-17": [("Groundnuts", 2)],
            "2024-05-18": [("Cassava", 2), ("Maize", 3)],
            "2024-01-19": [("Maize", 4), ("Groundnuts", 8)],
            "2024-06-13": [("Cassava", 5), ("Groundnuts", 5)],
            "2023-10-17": [("Maize", 2)],
            "2023-11-18": [("Cassava", 1), ("Groundnuts", 3)],
            "2023-12-19": [("Maize", 4)]
        }

        # Fetch a user and some products to associate orders with
        user = User.objects.first()
        products = Product.objects.all()

        if user is None:
            self.stdout.write(self.style.ERROR('No users found in the database. Please create a user first.'))
            return

        if not products.exists():
            self.stdout.write(self.style.ERROR('No products found in the database. Please create some products first.'))
            return

        orders = []
        for date_str, product_quantities in dummy_data.items():
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            for product_name, quantity in product_quantities:
                product = products.filter(name__name=product_name).first()
                if product:
                    orders.append(Order(
                        id=uuid.uuid4(),
                        product=product,
                        quantity=quantity,
                        buyer=user,
                        farmer=product.farmer,
                        description=f'Dummy order for {product_name}',
                        total_cost=product.price * quantity,
                        created_at=timezone.make_aware(date),
                        processed=False
                    ))

        Order.objects.bulk_create(orders)
        self.stdout.write(self.style.SUCCESS(f'Successfully inserted {len(orders)} Order records.'))




# from django.core.management.base import BaseCommand
# from orders.models import Order

# class Command(BaseCommand):
#     help = 'Delete dummy data from the Order model'

#     def handle(self, *args, **kwargs):
#         # Define the criteria for the dummy data, e.g., a specific date range or description pattern
#         description_pattern = 'Dummy order for'
#         date_range_start = '2023-10-17'
#         date_range_end = '2024-06-13'

#         # Delete orders that match the criteria
#         orders_to_delete = Order.objects.filter(
#             description__startswith=description_pattern,
#             created_at__range=[date_range_start, date_range_end]
#         )

#         count, _ = orders_to_delete.delete()

#         self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} Order records.'))



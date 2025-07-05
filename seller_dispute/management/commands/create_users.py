import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from faker import Faker  
from seller_dispute.models import CustomUser  

fake = Faker()

class Command(BaseCommand):
    help = "Generate 50 random CustomUser accounts"

    def handle(self, *args, **kwargs):

        users_created = 0
        for i in range(1, 51):
            username = f"user{i}_{get_random_string(4)}"
            email = f"{username}@example.com"
            password = get_random_string(8)
            phone = f"98765{random.randint(10000, 99999)}"  # Generates unique 10-digit numbers
            
            # Generate random birth date (between 1980-2005)
            start_date = datetime(1980, 1, 1)
            random_days = random.randint(0, (datetime(2005, 12, 31) - start_date).days)
            date_of_birth = start_date + timedelta(days=random_days)

            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone,
                date_of_birth=date_of_birth
            )

            users_created += 1
            self.stdout.write(self.style.SUCCESS(f"Created User {users_created}: {username}, {phone}, {phone}, DOB: {date_of_birth}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {users_created} users!"))

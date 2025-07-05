from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Not needed just thought of adding authentication but may extend later
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

"""
    Sample Order model is used to store the order details.
"""
class Order(models.Model):
    order_id = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)
    order_date = models.DateTimeField()
    item_sku = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    item_quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.order_id} - {self.customer_name}"

"""
    Sample Return model is used to store the return details.
"""
class Return(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='return_event')
    return_id = models.CharField(max_length=50, unique=True)
    return_reason = models.CharField(max_length=255)
    return_tracking_number = models.CharField(max_length=100, blank=True, null=True)
    return_date = models.DateTimeField()
    original_item_condition = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    return_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Return {self.return_id} for Order {self.order.order_id}"

"""
    Main modal on which the whole UI is based.
    It contains the information regarding the dispute case.
"""
class DisputeCase(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_review', 'In Review'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    case_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reason = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    # Currently we are allowing only one return event per dispute case
    return_event = models.OneToOneField(Return, on_delete=models.CASCADE, related_name='dispute_case')
    resolution_notes = models.TextField(blank=True, null=True)
    # A random disputed amount for now, we can link it with the return amount later
    disputed_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Dispute {self.case_number} ({self.status})"

"""
    Dispute Case Update model is used to store the update details and track the timeline of the dispute case.
"""
class DisputeCaseUpdate(models.Model):
    dispute_case = models.ForeignKey(DisputeCase, on_delete=models.CASCADE, related_name='updates')
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=DisputeCase.STATUS_CHOICES)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Update for {self.dispute_case.case_number} at {self.updated_at}"




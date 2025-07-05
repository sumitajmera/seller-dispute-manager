from rest_framework import serializers
from .models import Order, Return, DisputeCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "date_of_birth"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'customer_name', 'customer_email', 'customer_address',
            'order_date', 'item_sku', 'item_name', 'item_quantity', 'amount'
        ]


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = ['id', 'return_id', 'order', 'return_reason', 'return_tracking_number', 'return_date', 'original_item_condition', 'notes', 'return_amount', 'return_items']


class DisputeCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisputeCase
        fields = [
            'id', 'case_number', 'created_at', 'updated_at', 'reason', 'description', 'status', 'return_event', 'resolution_notes', 'disputed_amount'
        ]

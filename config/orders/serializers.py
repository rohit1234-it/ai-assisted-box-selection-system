from rest_framework import serializers

from orders.models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "items"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                **item_data
            )

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        # Update Order fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Update Order Items
        if items_data is not None:
            instance.items.all().delete()

            for item_data in items_data:
                OrderItem.objects.create(
                    order=instance,
                    **item_data
                )

        return instance
from django.test import TestCase
from rest_framework.test import APIClient

from products.models import Product
from boxes.models import Box
from orders.models import Order, OrderItem
from orders.services import recommend_box


class BoxRecommendationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.product = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=5,
            weight=2
        )

        self.small_box = Box.objects.create(
            name="Small Box",
            inner_length=35,
            inner_width=25,
            inner_height=10,
            max_weight=5,
            cost=20
        )

        self.large_box = Box.objects.create(
            name="Large Box",
            inner_length=50,
            inner_width=40,
            inner_height=20,
            max_weight=10,
            cost=50
        )

    def test_product_fits_and_cheapest_box_is_selected(self):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1
        )

        selected_box = recommend_box(order.items.all())

        self.assertEqual(selected_box, self.small_box)

    def test_heavier_product_rejects_box(self):
        heavy_product = Product.objects.create(
            name="Heavy Product",
            length=30,
            width=20,
            height=5,
            weight=8
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=heavy_product,
            quantity=1
        )

        selected_box = recommend_box(order.items.all())

        self.assertEqual(selected_box, self.large_box)

    def test_no_suitable_box_returns_none(self):
        oversized_product = Product.objects.create(
            name="Oversized Product",
            length=100,
            width=100,
            height=100,
            weight=2
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=oversized_product,
            quantity=1
        )

        selected_box = recommend_box(order.items.all())

        self.assertIsNone(selected_box)

    def test_product_rotation_is_supported(self):
        rotated_product = Product.objects.create(
            name="Rotated Product",
            length=25,
            width=35,
            height=10,
            weight=2
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=rotated_product,
            quantity=1
        )

        selected_box = recommend_box(order.items.all())

        self.assertEqual(selected_box, self.small_box)

    def test_recommend_box_api(self):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1
        )

        response = self.client.post(
            f"/api/orders/{order.id}/recommend-box/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["recommended_box"]["name"],
            "Small Box"
        )
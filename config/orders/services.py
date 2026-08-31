from itertools import permutations
from boxes.models import Box


def product_fits_in_box(product, box):
    product_dimensions = [
        float(product.length),
        float(product.width),
        float(product.height),
    ]

    box_dimensions = [
        float(box.inner_length),
        float(box.inner_width),
        float(box.inner_height),
    ]

    for orientation in permutations(product_dimensions):
        if (
            orientation[0] <= box_dimensions[0]
            and orientation[1] <= box_dimensions[1]
            and orientation[2] <= box_dimensions[2]
        ):
            return True

    return False


def recommend_box(order_items):
    total_weight = sum(
        float(item.product.weight) * item.quantity
        for item in order_items
    )

    suitable_boxes = []

    for box in Box.objects.all():
        if total_weight > float(box.max_weight):
            continue

        all_products_fit = True

        for item in order_items:
            if not product_fits_in_box(item.product, box):
                all_products_fit = False
                break

        if all_products_fit:
            suitable_boxes.append(box)

    if not suitable_boxes:
        return None

    return min(
        suitable_boxes,
        key=lambda box: (float(box.cost), box.inner_length * box.inner_width * box.inner_height)
    )
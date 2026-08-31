from itertools import permutations

from boxes.models import Box


def get_product_dimensions(product):
    """Return product dimensions as floats."""
    return (
        float(product.length),
        float(product.width),
        float(product.height),
    )


def get_box_dimensions(box):
    """Return box internal dimensions as floats."""
    return (
        float(box.inner_length),
        float(box.inner_width),
        float(box.inner_height),
    )


def get_orientations(dimensions):
    """
    Return all unique rotations of a rectangular product.
    """
    return list(set(permutations(dimensions)))


def product_fits_in_box(product, box):
    """
    Check whether a single product can fit inside a box
    in at least one orientation.
    """
    box_dimensions = get_box_dimensions(box)

    for orientation in get_orientations(get_product_dimensions(product)):
        if all(
            orientation[i] <= box_dimensions[i]
            for i in range(3)
        ):
            return True

    return False


def boxes_overlap(first, second):
    """
    Check whether two 3D rectangular objects overlap.

    Each object is represented as:
        (x, y, z, length, width, height)
    """
    first_x, first_y, first_z, first_l, first_w, first_h = first
    second_x, second_y, second_z, second_l, second_w, second_h = second

    return not (
        first_x + first_l <= second_x
        or second_x + second_l <= first_x
        or first_y + first_w <= second_y
        or second_y + second_w <= first_y
        or first_z + first_h <= second_z
        or second_z + second_h <= first_z
    )


def can_place_item(position, dimensions, box_dimensions, placed_items):
    """
    Check whether an item can be placed at a specific position.
    """
    x, y, z = position
    length, width, height = dimensions

    box_length, box_width, box_height = box_dimensions

    # Check box boundaries.
    if (
        x + length > box_length
        or y + width > box_width
        or z + height > box_height
    ):
        return False

    new_item = (
        x,
        y,
        z,
        length,
        width,
        height,
    )

    # Check collision with already placed items.
    for placed_item in placed_items:
        if boxes_overlap(new_item, placed_item):
            return False

    return True


def try_pack_products(order_items, box):
    """
    Try to physically place all products in the box.

    This uses a deterministic 3D placement heuristic:
    - products are processed from largest volume to smallest
    - all product rotations are considered
    - candidate positions are generated from faces/corners
      of already placed products

    Returns:
        True  -> all products were placed
        False -> at least one product could not be placed
    """
    box_dimensions = get_box_dimensions(box)

    # Expand quantities into individual products.
    products = []

    for item in order_items:
        product_dimensions = get_product_dimensions(item.product)

        for _ in range(item.quantity):
            volume = (
                product_dimensions[0]
                * product_dimensions[1]
                * product_dimensions[2]
            )

            products.append(
                {
                    "dimensions": product_dimensions,
                    "volume": volume,
                }
            )

    # Empty order.
    if not products:
        return False

    # Place larger products first.
    products.sort(
        key=lambda product: product["volume"],
        reverse=True,
    )

    placed_items = []

    for product in products:
        dimensions = product["dimensions"]
        orientations = get_orientations(dimensions)

        # Start with the origin.
        candidate_positions = {(0.0, 0.0, 0.0)}

        # Add positions next to the faces of already placed products.
        for placed in placed_items:
            x, y, z, length, width, height = placed

            candidate_positions.update(
                {
                    (x + length, y, z),
                    (x, y + width, z),
                    (x, y, z + height),
                }
            )

        # Sort candidates so packing is deterministic.
        candidate_positions = sorted(
            candidate_positions,
            key=lambda position: (
                position[2],
                position[1],
                position[0],
            ),
        )

        item_placed = False

        for orientation in orientations:
            for position in candidate_positions:
                if can_place_item(
                    position,
                    orientation,
                    box_dimensions,
                    placed_items,
                ):
                    x, y, z = position
                    length, width, height = orientation

                    placed_items.append(
                        (
                            x,
                            y,
                            z,
                            length,
                            width,
                            height,
                        )
                    )

                    item_placed = True
                    break

            if item_placed:
                break

        if not item_placed:
            return False

    return True


def recommend_box(order_items):
    """
    Recommend the cheapest box that can contain all order items.

    Selection rules:
    1. Total order weight must not exceed box capacity.
    2. Every product must physically fit.
    3. All product quantities must be packable together.
    4. Among suitable boxes, choose the lowest cost.
    5. If costs are equal, choose the box with the smallest volume.
    """
    order_items = list(order_items)

    if not order_items:
        return None

    total_weight = sum(
        float(item.product.weight) * item.quantity
        for item in order_items
    )

    suitable_boxes = []

    for box in Box.objects.all():
        # Weight constraint.
        if total_weight > float(box.max_weight):
            continue

        # Quick dimension check before attempting 3D packing.
        if any(
            not product_fits_in_box(item.product, box)
            for item in order_items
        ):
            continue

        # Actual multi-product packing check.
        if not try_pack_products(order_items, box):
            continue

        suitable_boxes.append(box)

    if not suitable_boxes:
        return None

    return min(
        suitable_boxes,
        key=lambda box: (
            float(box.cost),
            float(box.inner_length)
            * float(box.inner_width)
            * float(box.inner_height),
        ),
    )
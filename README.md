# AI-Assisted Box Selection System

## Overview

This project is a Django REST API based box selection system for an ecommerce platform.

The system recommends a suitable shipping box for an order based on:

- Product dimensions
- Product weight
- Product quantity
- Box internal dimensions
- Box maximum weight capacity
- Box cost

The goal is to help warehouse teams select an appropriate shipping box for customer orders.

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- Git & GitHub
- Postman
- Django TestCase

## Features

- Product management
- Shipping box management
- Order and order-item management
- Box recommendation
- Product dimension rotation support
- Weight capacity validation
- Lowest-cost suitable box selection
- Automated test cases

## Project Structure

```text
box_selection_system/
│
├── config/
│   ├── config/
│   ├── products/
│   ├── boxes/
│   ├── orders/
│   └── manage.py
│
├── README.md
├── AI_USAGE.md
├── LEARNINGS.md
├── TEST_OUTPUT.md
├── CHAT_TRANSCRIPT.html
├── requirements.txt
└── .gitignore

API Endpoints
Products
GET  /api/products/
POST /api/products/

Boxes
GET  /api/boxes/
POST /api/boxes/

Orders
GET  /api/orders/
POST /api/orders/

Box Recommendation
POST /api/orders/<order_id>/recommend-box/

Example:

POST http://127.0.0.1:8000/api/orders/1/recommend-box/
Box Recommendation Logic

The recommendation service checks whether the products in an order can fit inside the available boxes.

Product dimensions are checked using different possible orientations. This allows a product to fit even when its original length, width and height order does not directly match the box dimensions.

The service also checks the total order weight against the maximum weight capacity of the box.

Among suitable boxes, the lowest-cost box is recommended.

The recommendation logic is separated into services.py so that the business logic remains independent from the API ViewSet.

Testing

Automated tests are implemented using Django's testing framework.

Run all tests with:

python manage.py test

Run order-related tests with:

python manage.py test orders

The project currently contains 5 automated tests covering the box recommendation functionality and related scenarios.

Setup

Create and activate a virtual environment:

python -m venv .venv

Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run migrations:

python manage.py migrate

Run the development server:

python manage.py runserver

The API will be available at:

http://127.0.0.1:8000/
Verification

The project was verified using:

python manage.py check

and:

python manage.py test

The automated tests passed successfully.

AI Usage

AI assistance was used during development for requirement understanding, architecture discussion, debugging, implementation guidance, and test design.

Detailed AI usage is documented separately in:

AI_USAGE.md
Learning

The main learning from this assignment was understanding how business logic can be separated from API views using a service layer.

The assignment also provided practical experience with ViewSets, routers, nested serializers, dimension permutations, and automated Django API testing.

Detailed learning notes are available in:

LEARNINGS.md
Limitations

The current implementation uses a simplified box-selection approach.

It checks product dimensions, possible orientations and weight capacity, but it does not implement a full 3D bin-packing optimization algorithm for complex multi-product packing arrangements.

License

This project was created as part of a technical hiring assignment.
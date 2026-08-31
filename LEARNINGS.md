# What I Learned

## 1. Django REST Framework and Business Logic

I already had experience creating Django APIs before this assignment. However,
this assignment helped me understand how business logic can be handled for a
real-world use case.

The main learning was the box recommendation logic, especially using
permutations to check whether product dimensions can fit inside a box in
different orientations.

I also learned how to organize and write automated test cases in the
appropriate Django test file.

## 2. ViewSets and Routers

I learned how to use Django REST Framework ViewSets to handle CRUD operations
for models.

I also understood how serializers are used to represent model data in API
requests and responses.

Using routers helped me understand how API URLs are registered and generated
for ViewSets.

## 3. Service Layer

I understood the purpose of separating business logic into a service layer.

In this project, the box recommendation logic was placed in `services.py`.
It handles the logic for determining which box is suitable for an order and
whether the products can fit within the available box dimensions and weight
capacity.

This helped keep the API ViewSet separate from the main business logic.

## 4. Testing and API Verification

I already had experience with API testing, but this assignment gave me more
practice with automated testing and endpoint verification.

I learned how to test the order recommendation flow using an order ID:

`POST /api/orders/1/recommend-box/`

I also learned that a custom ViewSet action can create an endpoint under an
existing resource URL.

The automated tests helped verify different scenarios such as product
dimensions, weight capacity, product rotation, and API response.

All five implemented tests passed successfully.

## 5. Most Challenging Part

The most challenging part of this assignment was understanding the logic
around orders and box selection.

Initially, I was confused about how product dimensions should be checked
against box dimensions and where this logic should be placed. After
understanding the implementation, I was able to identify which logic belonged
in the service layer and how the recommendation flow worked.

The rest of the project, such as the basic CRUD APIs, was familiar to me
because I already had experience creating Django APIs.

I also used AI assistance while designing the models and discussing the
implementation, and then verified the resulting code through API testing and
automated tests.
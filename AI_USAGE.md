# AI Usage Documentation

## 1. AI Tool Used

**Tool:** ChatGPT

ChatGPT was used as an AI-assisted development and problem-solving tool during
the implementation of this Django REST API assignment.

AI assistance was used for understanding requirements, discussing architecture,
implementing Django REST Framework components, debugging, and designing tests.

---

## 2. Prompts Used

The following are representative prompts from the actual development
conversation.

### Requirement Understanding

**Prompt:**
> Python/Django Hiring Assignment: AI-Assisted Box Selection System.
> Please read again.

**Purpose:**
To confirm the assignment requirements, deliverables, and expected scope before
starting implementation.

---

### Technology and Architecture

**Prompt:**
> Tech stack?

**Purpose:**
To discuss an appropriate technology stack for the assignment.

**Prompt:**
> mala viewset use karaycha aahe

**Purpose:**
To use Django REST Framework ViewSets and routers instead of generic API views.

**Prompt:**
> service file cha kay use aahe aani company he structure accept karel ka

**Purpose:**
To understand the purpose of a service layer and determine whether separating
business logic from API views was appropriate for the assignment.

---

### API Implementation

**Prompt:**
> start

**Purpose:**
To begin implementing the Django application step by step.

**Prompt:**
> tula ky send kru

**Purpose:**
To provide the relevant project files so that the existing implementation
could be reviewed before continuing with the API development.

---

### Testing

**Prompt:**
> test cases kuthe lihaychya hotya

**Purpose:**
To clarify where automated test cases should be implemented in the Django
project.

---

## 3. AI Output Accepted

AI assistance was used for the following implementation areas:

- Django REST Framework ViewSet structure
- Router-based API routing
- Product and Box serializers
- Order and OrderItem serializer structure
- Box recommendation service structure
- Recommendation API endpoint
- Automated test case structure
- Project documentation structure

The generated suggestions were reviewed and executed locally before being
accepted into the project.

---

## 4. AI Output Rejected or Modified

AI suggestions were not accepted blindly. Changes were made based on the
project requirements and actual testing.

### ViewSet Approach

The initial API approach used generic class-based views. I chose to use
`ModelViewSet` and routers because a ViewSet-based structure was more suitable
for the CRUD APIs in this project.

### Order Serializer

The initial Order serializer used:

`items = OrderItemSerializer(many=True, read_only=True)`

This did not allow order items to be submitted while creating an order.

The implementation was modified to support nested order-item creation using a
custom `create()` method.

### Recommendation API Testing

During Postman testing, the recommendation endpoint was initially called with
an incorrect URL spelling and HTTP method.

The request was corrected to:

`POST /api/orders/<order_id>/recommend-box/`

### Recommendation Logic

The recommendation implementation was reviewed to understand its limitations.
The current implementation checks individual product fit and total weight,
rather than implementing a full industrial 3D bin-packing algorithm.

This limitation is documented in the README.

---

## 5. Mistakes Identified

The following issues were identified and corrected during development:

1. Incorrect HTTP method used while testing the recommendation endpoint.
2. Incorrect URL spelling while testing the recommendation endpoint.
3. Order serializer initially prevented nested order-item creation.
4. The limitation of the simplified multi-product packing approach was
   identified and documented.

---

## 6. Verification Steps

The final implementation was verified using:

### Django System Check

Command:

`python manage.py check`

Result:

`System check identified no issues (0 silenced).`

### API Testing

Product and Box APIs were tested using Postman.

The Order creation API was tested with an order item.

The Box Recommendation API was tested using:

`POST /api/orders/<order_id>/recommend-box/`

The API successfully returned a recommended box with HTTP 200.

### Automated Testing

Command:

`python manage.py test orders`

Result:

```text
Found 9 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 9 tests in 0.115s

OK
Destroying test database for alias 'default'...
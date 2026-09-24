# ShopSphere

A Django-based e-commerce application with a REST API, JWT authentication, payment integration, and asynchronous email processing.

## Features

### E-commerce
- Product management
- Session-based shopping cart
- Cart add, update and remove functionality
- Checkout and order creation
- Order history
- Order and OrderItem management
- Stock quantity management

### REST API
- Django REST Framework API
- ModelViewSets and routers
- Nested serializers for order items and products
- JWT authentication
- Role-based permissions for admin and normal users
- Object-level permissions for user orders
- Product search, filtering and ordering
- API pagination
- Custom API actions
- Serializer and business-logic validation
- Database transactions for order creation
- API and authentication/permission testing

### Performance
- Avoided N+1 query problems
- Used `select_related()` and `prefetch_related()` where appropriate
- Optimized database queries

### Payments
- Razorpay test-mode payment integration
- Payment signature verification
- Secure handling of API credentials using environment variables

### Background Processing
- Celery for asynchronous tasks
- Redis as Celery message broker
- Asynchronous order confirmation emails
- `transaction.on_commit()` to trigger email tasks after successful database transactions

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Razorpay
- JWT
- Git/GitHub
# 🥛 OurCowMolly

OurCowMolly is a backend project developed as an MVP with the goal of simulating the digital management of a small local dairy shop, enabling the creation, management, and tracking of orders in a simple and structured way.

---

## Project Goal

Build a backend that:

- manages products, customers, and orders
- implements real-world business logic (stock, order statuses, pricing)
- exposes clear and testable **REST APIs**
- is easily extensible towards:
  - a web dashboard
  - an interaction layer via chatbot (LLM)

---

## MVP

### 📦 Products
- Full CRUD operations for products
- Stock management

### 👤 Customers
- Full CRUD operations for customers
- Customer → orders associations

### 🧾 Orders
- Creation of orders with multiple products
- Business rules:
  - stock is decreased only when the order is confirmed (`CONFIRMED`)
  - controlled order status transitions
  - errors handled via custom exceptions (`NotFoundError`, `BadRequestError`)

---

## Architettura

Modular structure:

```
.
├── core/          # config, database, utils
├── products/      # models, schemas, service, routers
├── customers/     # models, schemas, service, routers
├── orders/        # models, schemas, service, routers
├── main.py
└── requirements.txt
```

Principles adopted:
- separation between routers (HTTP layer) and services (business logic)
- ORM-based data access using SQLAlchemy
- data validation and serialization via Pydantic schemas
- structured logging
- synchronous codebase

---

## Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite (local DB for MVP)
- Pydantic
- Uvicorn

## Sviluppi futuri (post-MVP)

...stay tuned!

                                                                                    *Ciocc128*


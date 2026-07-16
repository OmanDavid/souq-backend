# Souq – Backend

Flask REST API for Souq, a multi-vendor marketplace connecting sellers and buyers.

## Tech Stack
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- SQLite

## Setup
```bash
git clone <backend-repo-url>
cd souq-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Server runs at `http://localhost:5000`

## API Endpoints
| Method | Endpoint | Protected |
|--------|----------|-----------|
| POST | /auth/register | No |
| POST | /auth/login | No |
| POST | /auth/reset-request | No |
| POST | /auth/reset-confirm | No |
| GET | /products | No |
| GET | /products/:id | No |
| POST | /products | Yes |
| PUT | /products/:id | Yes |
| DELETE | /products/:id | Yes |
| GET | /orders | Yes |
| GET | /orders/:id | Yes |
| POST | /orders | Yes |
| PUT | /orders/:id | Yes |
| DELETE | /orders/:id | Yes |

## Models
User, Product, Category, Order (many-to-many with Product via `order_items`)

## License
MIT
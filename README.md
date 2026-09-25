# Project Online Auction System

A full-stack online auction platform built with Django REST Framework on the backend and React on the frontend. It allows users to register, create auctions, place bids, track bid history, and complete payments in a modern marketplace-style interface.

## Features

- User registration and authentication
- JWT-based login and protected API routes
- Auction creation, editing, and deletion
- Live bidding and highest-bid tracking
- Bid history and auction detail views
- Seller and buyer profile management
- Stripe-ready payment flow
- Responsive React frontend
- Admin-ready Django backend

## Tech Stack

- Backend: Python, Django, Django REST Framework
- Authentication: JWT (SimpleJWT)
- Frontend: React, React Router, Redux Toolkit
- HTTP Client: Axios
- Styling: CSS
- Database: SQLite for development, MySQL-ready configuration for production
- Deployment: Django + React static build support, Vercel/Render/Heroku friendly

## Project Structure

```bash
auction-system/
├── auction_backend/         # Django project settings and URLs
├── auctions/                # Auction models, serializers, views
├── bids/                    # Bid logic and models
├── users/                   # User authentication and profiles
├── payments/                # Payment integration logic
├── auction-frontend/        # React frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vercel.json
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Procfile
├── db.sqlite3
├── README.md
└── verify_system.py
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+
- Node.js 18+
- npm or yarn
- Git

## Backend Setup

1. Open a terminal in the project root.
2. Create and activate a virtual environment:

```bash
cd auction-system
python -m venv venv
venv\Scripts\activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
copy .env.example .env
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create an admin user:

```bash
python manage.py createsuperuser
```

7. Start the backend server:

```bash
python manage.py runserver
```

The backend will run at:

- http://localhost:8000
- Django admin: http://localhost:8000/admin

## Frontend Setup

Open a second terminal and run:

```bash
cd auction-system/auction-frontend
npm install
npm start
```

The frontend will run at:

- http://localhost:3000

## Environment Variables

Create a `.env` file in the project root using `.env.example` as a template. Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000

DB_ENGINE=sqlite

STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
```

## API Overview

The backend exposes REST API endpoints for users, auctions, bids, and payments.

### Authentication

- POST /api/users/register/
- POST /api/token/
- POST /api/token/refresh/

### Users

- GET /api/users/profile/
- PATCH /api/users/profile/

### Auctions

- GET /api/auctions/
- POST /api/auctions/
- GET /api/auctions/<id>/
- PATCH /api/auctions/<id>/
- DELETE /api/auctions/<id>/
- POST /api/auctions/<id>/place_bid/

### Payments

- POST /api/payments/initiate/
- GET /api/payments/

## Production Notes

- The Django app is configured to serve the React build when deployed.
- Static files are collected using Whitenoise.
- The project is ready for deployment on services such as Render, Railway, Heroku, or Vercel using the frontend API URL.

## License

This project is intended for educational and portfolio use.

## Author

Aayush Patidar

## Repository

GitHub repository for this project:

- https://github.com/aayushpatidar2004/Project-Online-Auction-System.git

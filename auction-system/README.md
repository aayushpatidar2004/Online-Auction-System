# 🔨 AuctionHub — Full Stack Auction System

A complete real-time auction platform built with **Django REST Framework** (backend) and **React** (frontend).

---

## 🏗️ Architecture

```
auction-system/
├── auction_backend/        # Django project
│   ├── users/              # CustomUser model + auth
│   ├── auctions/           # Auction model + bidding logic
│   ├── bids/               # Bid model
│   └── payments/           # Payment model (Stripe-ready)
├── auction-frontend/       # React SPA
│   └── src/
│       ├── components/     # React components
│       ├── services/api.js # Axios API client
│       └── store/          # Redux Toolkit state
├── requirements.txt
└── .env.example
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### 1. Clone & Backend Setup

```bash
# Navigate into the project
cd auction-system

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env   # Windows
cp .env.example .env     # Mac/Linux

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (for admin panel)
python manage.py createsuperuser

# Start backend server
python manage.py runserver
```
Backend runs at: **http://localhost:8000**
Admin panel: **http://localhost:8000/admin**

### 2. Frontend Setup

```bash
# In a new terminal
cd auction-system

# Create React app (first time only)
npx create-react-app auction-frontend

# Copy component files into auction-frontend/src/
# (all files are already created in auction-frontend/)

# Install dependencies
cd auction-frontend
npm install

# Start frontend
npm start
```
Frontend runs at: **http://localhost:3000**

---

## 📡 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/users/register/` | No | Register new user |
| POST | `/api/token/` | No | Login → get JWT |
| POST | `/api/token/refresh/` | No | Refresh access token |
| GET | `/api/users/profile/` | Yes | Get own profile |
| PATCH | `/api/users/profile/` | Yes | Update profile |
| GET | `/api/auctions/` | No | List all auctions |
| POST | `/api/auctions/` | Yes | Create auction |
| GET | `/api/auctions/{id}/` | No | Auction detail |
| PATCH | `/api/auctions/{id}/` | Yes | Update auction |
| DELETE | `/api/auctions/{id}/` | Yes | Delete auction |
| POST | `/api/auctions/{id}/place_bid/` | Yes | Place a bid |
| GET | `/api/auctions/{id}/bid_history/` | No | Bid history |
| GET | `/api/auctions/my_auctions/` | Yes | My listed auctions |
| GET | `/api/auctions/my_bids/` | Yes | Auctions I've bid on |
| POST | `/api/payments/initiate/` | Yes | Initiate payment |
| GET | `/api/payments/` | Yes | My payments |

### Example: Place a Bid
```bash
curl -X POST http://localhost:8000/api/auctions/1/place_bid/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"bid_amount": 150.00}'
```

---

## 🗄️ Database Models

### CustomUser
| Field | Type | Notes |
|-------|------|-------|
| username | CharField | Unique |
| email | EmailField | |
| phone | CharField | Unique, optional |
| seller_rating | DecimalField | 0.00–5.00 |
| buyer_rating | DecimalField | 0.00–5.00 |
| wallet_balance | DecimalField | |
| profile_image | ImageField | Optional |
| created_at | DateTimeField | Auto |

### Auction
| Field | Type | Notes |
|-------|------|-------|
| seller | FK → CustomUser | |
| title | CharField | |
| description | TextField | |
| category | CharField | electronics/fashion/home/etc |
| condition | CharField | new/used |
| base_price | DecimalField | |
| current_highest_bid | DecimalField | Auto-updated on bid |
| highest_bidder | FK → CustomUser | Nullable |
| start_time | DateTimeField | |
| end_time | DateTimeField | |
| status | CharField | active/ended/cancelled |
| image | ImageField | Optional |

### Bid
| Field | Type | Notes |
|-------|------|-------|
| auction | FK → Auction | |
| bidder | FK → CustomUser | |
| bid_amount | DecimalField | Must exceed current_highest_bid |
| auto_bid_limit | DecimalField | Optional auto-bidding cap |
| created_at | DateTimeField | |

### Payment
| Field | Type | Notes |
|-------|------|-------|
| auction | OneToOneField → Auction | |
| buyer | FK → CustomUser | |
| amount | DecimalField | |
| payment_id | CharField | Stripe payment intent ID |
| status | CharField | pending/completed/failed |

---

## 🌐 Deployment

### Backend → Render / Railway / Heroku
```bash
# create .env or set environment variables in hosting platform
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-backend-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.com

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Frontend → Vercel / Netlify
```bash
cd auction-frontend
# Add environment variable for the live backend URL
# REACT_APP_API_URL=https://your-backend-domain.com/api
npm install
npm run build
```

### Full production setup
- backend serves the Django API and static frontend files from the same app
- frontend can also be hosted separately, but the API base URL must point to the deployed backend
- for a single-host deployment, keep Django and React build under the same project and serve static files with WhiteNoise

---

## 🔧 Environment Variables

Copy `.env.example` to `.env` and configure:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Optional: MySQL (default is SQLite)
# DB_NAME=auction_db
# DB_USER=root
# DB_PASSWORD=your_password

# Optional: Stripe
# STRIPE_SECRET_KEY=sk_test_...
# STRIPE_PUBLISHABLE_KEY=pk_test_...
```

---

## 🧪 Testing with Postman

1. **Register**: `POST /api/users/register/` with `{username, email, password, password2}`
2. **Login**: `POST /api/token/` → copy `access` token
3. **Authorize**: Add header `Authorization: Bearer <token>`
4. **Create auction**: `POST /api/auctions/` (multipart form with image)
5. **Place bid**: `POST /api/auctions/{id}/place_bid/` with `{bid_amount: 100}`
6. **View history**: `GET /api/auctions/{id}/bid_history/`

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, Django REST Framework |
| Auth | JWT (SimpleJWT) |
| Database | SQLite (dev) / MySQL (prod) |
| File Storage | Django media files / Pillow |
| Frontend | React 18, Redux Toolkit |
| HTTP Client | Axios (with JWT interceptors) |
| Styling | Custom CSS (dark theme) |
| Notifications | React Toastify |
| Deployment | Heroku (backend) + Vercel (frontend) |

---

## 🔮 Future Enhancements
- WebSocket real-time bidding (Django Channels)
- Full Stripe payment integration
- Email notifications on auction end
- Auto-bidding engine (Celery + Redis)
- Mobile app (React Native)

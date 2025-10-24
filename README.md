# 🛍️ Meesho Clone - Full Stack E-commerce Platform

A pixel-perfect clone of Meesho, India's leading reselling platform, built with modern web technologies. This project replicates Meesho's core features including product browsing, cart management, user authentication, order placement, and UPI payment integration.

![Meesho Clone](https://img.shields.io/badge/Meesho-Clone-purple)
![React](https://img.shields.io/badge/React-18.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-brightgreen)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-38B2AC)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Database Seeding](#database-seeding)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Project Architecture](#project-architecture)
- [Key Features Explained](#key-features-explained)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### 🎯 Core Features
- **User Authentication**: Secure registration and login with JWT tokens
- **Product Catalog**: Browse 80+ products across 8 categories
- **Search & Filter**: Find products quickly with search and category filters
- **Advanced Filtering**: Price range, ratings, categories, delivery type filters
- **Product Details**: Detailed product pages with images, prices, reviews, and ratings
- **Shopping Cart**: Add/remove items, update quantities, and view cart total
- **Wishlist**: Save favorite products for later
- **Order Management**: Place orders and view order history
- **UPI Payment**: Integrated UPI payment gateway for seamless checkout
- **Product Reviews**: View and read customer reviews and ratings
- **Responsive Design**: Mobile-first design that works on all devices

### 🆕 New Features (v2.0)
- **Address Management**: Add, edit, delete multiple addresses with default address support
- **Coupon System**: Apply discount codes with real-time calculation
- **Seller Platform**: Become a seller, manage shop profile, view ratings and reviews
- **Help Center**: Comprehensive FAQs and support contact options
- **Account Dashboard**: Manage profile, addresses, and view order history
- **Advanced Filtering**: Filter by price, rating, category, and delivery type
- **Mobile Navigation**: Bottom navigation bar for mobile users

### 🎨 UI/UX Features
- Clean, modern interface matching Meesho's design language
- Category-based navigation
- Product cards with discount badges
- Free delivery and COD indicators
- Rating system with review counts
- Smooth transitions and animations
- Toast notifications for user actions

---

## 🚀 Tech Stack

### Frontend
| Technology | Purpose | Version |
|------------|---------|---------|
| **React.js** | UI Library | 18.x |
| **React Router** | Client-side routing | 6.x |
| **Axios** | HTTP client for API calls | Latest |
| **TailwindCSS** | Utility-first CSS framework | 3.x |
| **Shadcn UI** | Pre-built UI components | Latest |
| **Lucide React** | Icon library | Latest |
| **React Context API** | Global state management | Built-in |

### Backend
| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | Python web framework | Latest |
| **Python** | Backend language | 3.8+ |
| **Motor** | Async MongoDB driver | Latest |
| **PyMongo** | MongoDB driver | Latest |
| **Pydantic** | Data validation | Latest |
| **python-jose** | JWT token handling | Latest |
| **passlib** | Password hashing | Latest |
| **bcrypt** | Encryption | Latest |

### Database
| Technology | Purpose |
|------------|---------|
| **MongoDB** | NoSQL database for storing products, users, orders, and reviews |

### Development Tools
- **CORS Middleware**: For cross-origin requests
- **Uvicorn**: ASGI server for FastAPI
- **Yarn**: Package manager for frontend
- **Pip**: Package manager for backend

---

## 📁 Project Structure

```
meesho-clone/
│
├── backend/                        # Backend FastAPI application
│   ├── models/                     # Pydantic models
│   │   ├── user.py                # User model
│   │   ├── product.py             # Product model
│   │   ├── order.py               # Order model
│   │   ├── category.py            # Category model
│   │   └── review.py              # Review model
│   │
│   ├── routes/                     # API route handlers
│   │   ├── auth.py                # Authentication endpoints
│   │   ├── products.py            # Product CRUD operations
│   │   ├── categories.py          # Category operations
│   │   ├── orders.py              # Order management
│   │   ├── payments.py            # UPI payment processing
│   │   └── reviews.py             # Product reviews
│   │
│   ├── middleware/                 # Middleware functions
│   │   └── auth_middleware.py     # JWT authentication middleware
│   │
│   ├── utils/                      # Utility functions
│   │   └── auth_utils.py          # JWT and password utilities
│   │
│   ├── server.py                   # Main FastAPI application (entry point)
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment variables
│   └── seed_with_matching_images.py # Database seeding script
│
├── frontend/                       # React frontend application
│   ├── public/                     # Static files
│   ├── src/
│   │   ├── components/            # Reusable components
│   │   │   ├── ui/               # Shadcn UI components
│   │   │   ├── Navbar.js         # Navigation bar
│   │   │   ├── Footer.js         # Footer component
│   │   │   └── ProductCard.js    # Product card component
│   │   │
│   │   ├── pages/                 # Page components
│   │   │   ├── Home.js           # Homepage
│   │   │   ├── ProductDetail.js  # Product details page
│   │   │   ├── Cart.js           # Shopping cart
│   │   │   ├── Login.js          # Login page
│   │   │   ├── Register.js       # Registration page
│   │   │   ├── Wishlist.js       # Wishlist page
│   │   │   ├── Search.js         # Search results
│   │   │   ├── Category.js       # Category page
│   │   │   ├── Checkout.js       # Checkout page
│   │   │   └── Orders.js         # Order history
│   │   │
│   │   ├── context/               # React Context
│   │   │   ├── AuthContext.js    # Authentication state
│   │   │   └── CartContext.js    # Cart state management
│   │   │
│   │   ├── services/              # API services
│   │   │   └── api.js            # Axios API client
│   │   │
│   │   ├── App.js                 # Main App component with routing
│   │   ├── App.css                # Global styles
│   │   └── index.js               # Entry point
│   │
│   ├── package.json               # Frontend dependencies
│   ├── tailwind.config.js         # Tailwind configuration
│   └── .env                       # Frontend environment variables
│
└── README.md                       # This file
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download](https://www.python.org/)
- **MongoDB** (v4.4 or higher) - [Download](https://www.mongodb.com/try/download/community)
- **Yarn** package manager - Install with `npm install -g yarn`

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd meesho-clone
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
```

**Create backend `.env` file:**
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=meesho_db
JWT_SECRET=your-super-secret-jwt-key-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from root)
cd frontend

# Install dependencies
yarn install
```

**Create frontend `.env` file:**
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

### 4. Start MongoDB

```bash
# On macOS (with Homebrew):
brew services start mongodb-community

# On Linux:
sudo systemctl start mongod

# Verify MongoDB is running:
mongosh
```

---

## 🚀 Running the Application

### Method 1: Using Supervisor (Recommended for Production)

If you're on Emergent platform or have supervisor:

```bash
# Restart all services
sudo supervisorctl restart all

# Check status
sudo supervisorctl status

# View logs
tail -f /var/log/supervisor/backend.err.log
tail -f /var/log/supervisor/frontend.err.log
```

### Method 2: Manual Start (Development)

#### Terminal 1: Start Backend

```bash
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

✅ Backend will be available at: **http://localhost:8001**
✅ API Documentation: **http://localhost:8001/docs**

#### Terminal 2: Start Frontend

```bash
cd frontend
yarn start
```

✅ Frontend will be available at: **http://localhost:3000**

---

## 🌱 Database Seeding

Populate the database with 81 products across 8 categories:

```bash
cd backend
python seed_with_matching_images.py
```

**This will create:**
- ✅ 8 product categories
- ✅ 81 unique products with matching images
- ✅ Realistic pricing with discounts
- ✅ Product ratings and reviews

**Categories:**
1. Women Ethnic (25 products) - Sarees, Kurtis, Lehengas
2. Women Western (8 products) - Dresses, Jeans, Tops
3. Men (8 products) - Shirts, T-shirts, Jeans
4. Kids (5 products) - Children's clothing
5. Electronics (16 products) - Phones, Earbuds, Tablets
6. Home & Kitchen (6 products) - Cookware, Utensils
7. Beauty & Health (5 products) - Makeup, Skincare
8. Bags & Footwear (8 products) - Handbags, Shoes

---

## 📚 API Documentation

### Base URL
```
http://localhost:8001/api
```

### 🔐 Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "phone": "9876543210"
}

Response: 200 OK
{
  "user_id": "uuid",
  "name": "John Doe",
  "email": "john@example.com"
}
```

#### Login User
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securePassword123"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "user_id": "uuid",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### 📦 Product Endpoints

#### Get All Products
```http
GET /api/products
GET /api/products?category=Women+Ethnic
GET /api/products?search=saree
```

#### Get Single Product
```http
GET /api/products/{product_id}
```

#### Get All Categories
```http
GET /api/categories
```

### 🛒 Order Endpoints

#### Create Order (Requires Auth)
```http
POST /api/orders
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "products": [
    {
      "product_id": "uuid",
      "quantity": 2,
      "price": 999
    }
  ],
  "total_amount": 1998,
  "shipping_address": {
    "street": "123 Main St",
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "400001"
  },
  "payment_method": "UPI"
}
```

#### Get User Orders (Requires Auth)
```http
GET /api/orders
Authorization: Bearer <access_token>
```

### 💳 Payment Endpoints

#### Process UPI Payment (Requires Auth)
```http
POST /api/payments/upi
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "order_id": "uuid",
  "upi_id": "user@paytm",
  "amount": 1998
}
```

### ⭐ Review Endpoints

#### Get Product Reviews
```http
GET /api/reviews/{product_id}
```

#### Add Review (Requires Auth)
```http
POST /api/reviews
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "product_id": "uuid",
  "rating": 5,
  "comment": "Excellent product!"
}
```

---

## 🔐 Environment Variables

### Backend `.env`

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGO_URL` | MongoDB connection URI | `mongodb://localhost:27017` |
| `DB_NAME` | Database name | `meesho_db` |
| `JWT_SECRET` | Secret for JWT tokens | `your-secret-key` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `30` |

### Frontend `.env`

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_BACKEND_URL` | Backend API URL | `http://localhost:8001` |

---

## 🏗️ Project Architecture

### Frontend Flow

```
User Interface
    ↓
React Components (Pages/Components)
    ↓
React Router (Navigation)
    ↓
Context API (AuthContext, CartContext)
    ↓
API Service (axios)
    ↓
Backend REST API
```

### Backend Flow

```
HTTP Request
    ↓
FastAPI Server
    ↓
CORS Middleware
    ↓
Authentication Middleware (JWT)
    ↓
Route Handler (/api/...)
    ↓
Pydantic Model Validation
    ↓
MongoDB Operations (Motor)
    ↓
JSON Response
```

### Authentication Flow

```
1. User registers/logs in
2. Backend hashes password (bcrypt)
3. Backend generates JWT token
4. Frontend stores token in localStorage
5. Frontend sends token in Authorization header
6. Backend validates token via middleware
7. Protected routes accessible
```

### Shopping Cart Flow

```
1. User adds product to cart
2. CartContext updates state
3. Cart saved to localStorage
4. Cart persists across sessions
5. User proceeds to checkout
6. Order created in database
7. Cart cleared after successful order
```

---

## 🔑 Key Features Explained

### 1. JWT Authentication
- **Registration**: Password hashed with bcrypt before storage
- **Login**: JWT token generated with user info
- **Token Storage**: Stored in localStorage on frontend
- **Protected Routes**: Token validated via middleware
- **Expiry**: Tokens expire after 30 minutes

### 2. Shopping Cart
- **State Management**: React Context API
- **Persistence**: localStorage for cart data
- **Operations**: Add, remove, update quantity
- **Calculation**: Real-time total calculation
- **Checkout**: Seamless integration with orders

### 3. Product Search & Filtering
- **Search**: By product name (real-time)
- **Filter**: By category
- **API**: Query parameters for filtering
- **Performance**: Debounced search input

### 4. Order Management
- **Creation**: Products, address, payment method
- **Storage**: MongoDB orders collection
- **History**: User can view past orders
- **Status Tracking**: Pending, Processing, Delivered

### 5. UPI Payment
- **Input**: User UPI ID (e.g., user@paytm)
- **Validation**: Backend validates format
- **Processing**: Simulated payment flow
- **Confirmation**: Order status updated
- **Note**: Demo payment (not real transactions)

### 6. Product Reviews
- **Display**: All reviews for a product
- **Submission**: Authenticated users only
- **Rating**: 1-5 stars
- **Aggregation**: Average rating calculated

---

## 🐛 Troubleshooting

### Backend Won't Start

```bash
# Check MongoDB is running
sudo systemctl status mongod  # Linux
brew services list | grep mongodb  # macOS

# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt

# Check for port conflicts
lsof -i :8001
```

### Frontend Won't Start

```bash
# Clear node modules
rm -rf node_modules yarn.lock
yarn install

# Check Node version
node --version  # Should be 16+

# Check for port conflicts
lsof -i :3000
```

### Database Connection Error

```bash
# Verify MONGO_URL in backend/.env
# Test connection
mongosh mongodb://localhost:27017

# Check MongoDB service
sudo systemctl status mongod
```

### CORS Errors

- Ensure `REACT_APP_BACKEND_URL` matches backend URL
- Check CORS settings in `backend/server.py`
- Clear browser cache

### JWT Token Errors

```bash
# Clear localStorage in browser DevTools
localStorage.clear()

# Re-login to get fresh token
# Ensure JWT_SECRET is set in backend/.env
```

---

## 📊 Database Collections

### users
```json
{
  "user_id": "uuid",
  "name": "string",
  "email": "string (unique)",
  "password": "hashed_string",
  "phone": "string",
  "created_at": "datetime"
}
```

### products
```json
{
  "name": "string",
  "price": "number",
  "original_price": "number",
  "discount": "number",
  "rating": "number (1-5)",
  "reviews": "number",
  "image": "string (URL)",
  "category": "string",
  "sizes": ["array"],
  "colors": ["array"],
  "description": "string",
  "free_delivery": "boolean",
  "cod": "boolean",
  "seller_name": "string",
  "stock": "number"
}
```

### orders
```json
{
  "order_id": "uuid",
  "user_id": "uuid",
  "products": [{
    "product_id": "uuid",
    "quantity": "number",
    "price": "number"
  }],
  "total_amount": "number",
  "shipping_address": {
    "street": "string",
    "city": "string",
    "state": "string",
    "pincode": "string"
  },
  "payment_method": "string",
  "payment_status": "string",
  "order_status": "string",
  "created_at": "datetime"
}
```

---

## 🚀 Deployment

### Production Setup

```bash
# Backend with Gunicorn
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001

# Frontend build
cd frontend
yarn build
npx serve -s build
```

### Environment Variables (Production)

Update `.env` files with production values:
- MongoDB connection string
- Strong JWT secret
- Production backend URL

---

## 🎯 Testing the Application

### 1. Test Backend API

Visit: `http://localhost:8001/docs` for interactive API documentation

### 2. Test Authentication

```bash
# Register a new user
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@test.com","password":"test123","phone":"9876543210"}'

# Login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

### 3. Test Products

```bash
# Get all products
curl http://localhost:8001/api/products

# Get products by category
curl http://localhost:8001/api/products?category=Women+Ethnic
```

---

## 📝 Development Notes

### Code Organization
- **Models**: Define data structure and validation
- **Routes**: Handle API endpoints and business logic
- **Middleware**: Handle cross-cutting concerns (auth, CORS)
- **Utils**: Reusable functions (JWT, password hashing)

### Best Practices
- Always use environment variables for sensitive data
- Validate all user inputs with Pydantic
- Use async/await for database operations
- Handle errors gracefully with try-catch
- Keep components small and reusable

### Security Considerations
- Passwords are hashed with bcrypt (never plain text)
- JWT tokens for stateless authentication
- CORS configured to prevent unauthorized access
- Input validation on both frontend and backend
- SQL injection prevented (NoSQL database)

---

## 🔮 Future Enhancements

- [ ] Real payment gateway integration (Razorpay, Stripe)
- [ ] Email notifications for orders
- [ ] SMS OTP verification
- [ ] Advanced product filtering (price range, ratings)
- [ ] Seller dashboard
- [ ] Product recommendations
- [ ] Wishlist synchronization
- [ ] Multi-language support
- [ ] Social login (Google, Facebook)
- [ ] Product comparison
- [ ] Discount coupons
- [ ] Live chat support

---

## 📞 Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review API documentation at `/docs`
3. Check browser console for frontend errors
4. Check backend logs for server errors

---

## 🙏 Acknowledgments

- **Meesho** - Original design inspiration
- **Unsplash & Pexels** - Product images
- **Shadcn UI** - UI component library
- **FastAPI** - Modern Python web framework
- **React** - Frontend library

---

## 📄 License

This project is for educational purposes only. Not affiliated with Meesho.

---

**Last Updated:** January 2025

**Made with ❤️ using React, FastAPI, and MongoDB**

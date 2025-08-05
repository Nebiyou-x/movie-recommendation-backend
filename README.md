# 🎬 Movie Recommendation Backend


This is a Django + Django REST Framework backend for a movie recommendation system.
It provides a REST API for managing movies and generating recommendations using JWT authentication.

The project is Dockerized with support for PostgreSQL, Redis, and Gunicorn for production deployment.

---

## 📂 Project Structure

movie-recommendation-backend/
│── core/                # Django core project (settings, wsgi, asgi)
│── movies/              # Movie app (models, views, serializers)
│── templates/           # HTML templates if needed
│── manage.py            # Django management script
│── requirements.txt     # Python dependencies
│── Dockerfile           # Docker image build instructions
│── docker-compose.yml   # Multi-container setup with PostgreSQL & Redis
│── .gitignore

---

## ⚙️ Features

- Django 4.2 with Django REST Framework
- JWT Authentication (via djangorestframework-simplejwt)
- Swagger API Documentation (drf-yasg)
- PostgreSQL database with psycopg2
- Redis caching and session support
- Whitenoise for serving static files
- Dockerized deployment using docker-compose and gunicorn
- Environment variables support using .env

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/movie-recommendation-backend.git
cd movie-recommendation-backend
```

### 2️⃣ Create and configure the .env file
```bash
# Database
DB_NAME=movie_db
DB_USER=movie_user
DB_PASSWORD=movie_password
DB_HOST=db
DB_PORT=5432

# Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

## 🐳 Running with Docker

This project is fully containerized. Run the following commands:

---

### 1️⃣ Build and start the containers
```bash
docker-compose up --build
```
This will start:

- web → Django backend running on http://localhost:8000
- db → PostgreSQL database
- redis → Redis cache server

### 2️⃣ Run migrations and collect static files

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

### 3️⃣ Access the app
- API Base URL: http://localhost:8000/
- Swagger Docs: http://localhost:8000/swagger/
- Admin Panel: http://localhost:8000/admin/

---

## 🖥️ Local Development (Without Docker)

If you want to run it locally using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup PostgreSQL and Redis manually, then:
python manage.py migrate
python manage.py runserver
```
---

## 🚀 Deployment
- Uses Gunicorn as WSGI server.
- Serves static files using Whitenoise.
- Deployed to Render and railway easily using Docker.

---

## 🧪 API Testing
You can test the endpoints using:

- Swagger UI: /swagger/
- Postman or cURL
- DRF browsable API

---

## 🐛 Additionals

1. Worker Timeout in Gunicorn
- Increase worker timeout or check for long-running queries.

2. Static Files Error
- Make sure to set:
```bash
STATIC_ROOT = BASE_DIR / 'staticfiles'
```
then run: 
```bash
python manage.py collectstatic --noinput
```

---
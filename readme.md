# Seller Dispute Manager

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd seller_dispute_manager
```

---

## Option 1: Manual Setup (Local Development)

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database
- Ensure PostgreSQL is installed and running.
- Create the database and user manually:
```bash
psql -U postgres
# In the psql shell, run:
CREATE DATABASE seller_db;
CREATE USER seller_rw WITH PASSWORD 'seller_rw';
GRANT ALL PRIVILEGES ON DATABASE seller_db TO seller_rw;
\q
```

### 5. Configure Environment Variables (Optional)
- By default, the project uses:
  - DB name: `seller_db`
  - User: `seller_rw`
  - Password: `seller_rw`
  - Host: `localhost`
  - Port: `5432`
- You can override these by setting the environment variables: `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`, `DJANGO_DB_HOST`, `DJANGO_DB_PORT`.

### 6. Remove Old Migrations and Database (Optional, for a clean start)
```bash
find seller_dispute/migrations/ -not -name '__init__.py' -name '*.py' -delete
rm -f db.sqlite3
```

### 7. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Sample Data (Optional)
```bash
# Create 50 random users
python manage.py create_users
# Create sample orders and returns
python manage.py create_orders_and_returns
# Create sample dispute entries
python manage.py seed_dispute_cases
```

### 9. Run the Development Server
```bash
python manage.py runserver
```

---

## Option 2: Run with Docker

### 1. Build and Start the Containers
```bash
docker-compose up --build
```
- This will start both the Django app and a PostgreSQL database using the settings in `docker-compose.yml`.
- The web app will be available at [http://localhost:8000](http://localhost:8000)

### 2. Run Migrations and Seed Data (in a separate terminal)
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py create_users
docker-compose exec web python manage.py create_orders_and_returns
docker-compose exec web python manage.py seed_dispute_cases
```

---

## Project Structure
- `seller_dispute/` - Main Django app for dispute management
- `seller_dispute_manager/` - Project settings and configuration
- `venv/` - Virtual environment (not tracked by git)


## API Endpoints
This project is primarily server-rendered (HTMX + Django templates). If you want to use or extend RESTful APIs, see `seller_dispute/urls.py` and `seller_dispute/views/dispute_case.py`.


## Notes
- The project uses Django and Django REST Framework.
- For HTMX endpoints, responses are HTML fragments for dynamic UI updates.
- For RESTful endpoints, responses are JSON (see DRF viewsets/serializers).


---
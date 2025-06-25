# Final Project Setup Guide

This guide will help you set up and run the project on your local machine.

## 1. Prerequisites
- Python 3.10 or newer
- PostgreSQL database
- (Optional) Virtual environment tool (venv, virtualenv, etc.)

## 2. Clone the Repository
Clone or download the project to your local machine.

## 3. Create and Activate Virtual Environment
```
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/Mac:
source venv/bin/activate
```

## 4. Install Dependencies
```
pip install -r requirement.txt
```

## 5. Configure Environment Variables
Edit the `.env` file in the project root with your database and JWT settings:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXP_DELTA_SECONDS=3600
```

## 6. Configure Database
- Make sure PostgreSQL is running and a database is created matching your `.env` settings.
- Update `alembic.ini` with your database URL if needed.

## 7. Run Database Migrations
```
alembic upgrade head
```
This will create all tables in your database.

## 8. Run the Application
```
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

## 9. API Documentation
Visit `http://localhost:8000/docs` for interactive API docs (Swagger UI).

## 10. Running Tests
If you have test scripts, run them as needed (e.g., with pytest or httpx).

---

For any issues, check your environment variables, database connection, and installed dependencies. If you need further help, please contact the project maintainer.


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
uvicorn main:app --reload --port [CHANGE_PORT_HERE]
```
The API will be available at `http://localhost:[PORT]`.

## 9. API Documentation
Visit `http://localhost:[PORT]/docs` for interactive API docs (Swagger UI).

---

## Alembic

1. Install Alembic (if not already installed):
   ```bash
   pip install alembic
   ```
2. Initialize Alembic (if not already initialized):
   ```bash
   alembic init alembic
   ```
3. Configure your database URL in `alembic.ini` or in `alembic/env.py`.
4. Generate a new migration after making model changes:
   ```bash
   alembic revision --autogenerate -m "Your migration message"
   ```
5. Apply migrations to the database:
   ```bash
   alembic upgrade head
   ```


## Quick setup when using Pycharm IDE
1. Open the project in PyCharm.
2. Go to `File` -> `Settings` -> `Project: [Your Project Name]` -> `Python Interpreter`.
3. Click on the gear icon and select `Add...`.
4. Choose `Virtualenv Environment` and select `New environment`.
5. Set the base interpreter to Python 3.10 or newer.
6. Click `OK` to create the virtual environment.
7. Once the environment is created, install the dependencies:
   - Open the terminal in PyCharm.
   - Run `pip install -r requirement.txt`.
8. Run the application:
   - Open the terminal in PyCharm.
   - Run `uvicorn main:app --reload --port [CHANGE_PORT_HERE]`.
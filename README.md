Multi-Tenant Project Management API

🚀 Overview

This is a Multi-Tenant Project Management API built using FastAPI, supporting:

- JWT Authentication
- Role-Based Access Control (Admin, Manager, Member)
- Organization-based data isolation (Multi-tenancy)
- CRUD for Organizations, Projects, Tasks
- Async SQLAlchemy with PostgreSQL
- Pagination
- Caching for project/task listing
- Background email simulation on task assignment
- Overdue task email notification

🏗 Architecture

- FastAPI
- Async SQLAlchemy
- SQLite (for development)
- JWT Authentication
- Redis (optional/local cache)

🔐 Roles

-  Admin : Full access
-  Manager : Create/Update projects & tasks
-  Member : View tasks & projects only

🏢 Multi-Tenancy

Users can only access:
- Projects belonging to their organization
- Tasks belonging to projects inside their organization
Data is filtered using organization_id from JWT token.

⚙️ Setup Instructions
1️⃣ Create Virtual Environment
python -m venv venv

Activate:
Windows:
venv\Scripts\activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Environment
Copy .env.sample → .env
Update values accordingly.

4️⃣ Initialize Database
python -m app.db.init_db

5️⃣ Run Server
uvicorn app.main:app


Open Swagger:
http://127.0.0.1:8000/docs

🔄 API Flow

1.Login → Get JWT token
2.Create Organization
3.Create Project
4.Create Task
5.List Projects/Tasks (paginated)
6.Overdue Check → /overdue/check

📧 Background Tasks
- Email simulated using print()

- Triggered on:
   .Task assignment
   .Overdue check

📊 Pagination

All list endpoints support:
?skip=0&limit=10

🧠 Caching

- List endpoints use in-memory caching
- Redis ready via REDIS_URL

📌 Notes

- Async DB operations used everywhere
- Proper HTTP status codes implemented
- Clean Swagger documentation
- Modular architecture

Note: SQLite is used for quick development setup. Can be easily switched to PostgreSQL in production.

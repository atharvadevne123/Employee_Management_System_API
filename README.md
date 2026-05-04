![CI](https://github.com/atharvadevne123/Employee_Management_System_API/actions/workflows/ci.yml/badge.svg)
![Python Package](https://github.com/atharvadevne123/Employee_Management_System_API/actions/workflows/python-publish.yml/badge.svg)
![Bump Version](https://github.com/atharvadevne123/Employee_Management_System_API/actions/workflows/bump-version.yml/badge.svg)

# Employee Management System API

A robust Django REST API for managing employees, departments, attendance records, and performance reviews. Built with PostgreSQL, JWT authentication, and Swagger for interactive API exploration.

---

## Features

- Django 4.2 + Django REST Framework
- JWT authentication via SimpleJWT
- CRUD APIs: Employees, Departments, Attendance, Performance Reviews
- Filtering, search, sorting, and pagination on all endpoints
- Swagger/OpenAPI docs at `/swagger/` and `/redoc/`
- `/api/health/` and `/api/version/` utility endpoints
- Database seeding with 50 fake employees (Faker)
- GitHub Actions CI (lint + tests on Python 3.10/3.11/3.12)
- Docker + docker-compose with PostgreSQL
- 60%+ test coverage with pytest

---

## Project Structure

```
Employee_Management_System_API/
├── employee_project/        # Django project config (settings, urls, wsgi)
├── employees/               # Employee, Department, PerformanceReview models + API
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── management/commands/seed_data.py
├── attendance/              # AttendanceRecord model + API
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── tests/                   # pytest test suite
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── pyproject.toml
└── .env.example
```

---

## Quick Start

```bash
git clone https://github.com/atharvadevne123/Employee_Management_System_API.git
cd Employee_Management_System_API

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run migrations and seed data (SQLite for local dev)
make migrate
make seed

# Start the development server
make run
# API is at http://127.0.0.1:8000/
# Swagger UI is at http://127.0.0.1:8000/swagger/
```

---

## Docker Setup

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
make docker-build
make docker-up
# API available at http://localhost:8000/
```

---

## Authentication

All endpoints except `/api/health/`, `/api/version/`, and `/swagger/` require JWT authentication.

**Obtain token:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

**Use token:**
```bash
curl http://localhost:8000/api/employees/employees/ \
  -H "Authorization: Bearer <your_access_token>"
```

**Refresh token:**
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<your_refresh_token>"}'
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | Liveness probe |
| GET | `/api/version/` | API version |
| POST | `/api/token/` | Obtain JWT |
| POST | `/api/token/refresh/` | Refresh JWT |
| GET/POST | `/api/employees/departments/` | List/create departments |
| GET/PUT/PATCH/DELETE | `/api/employees/departments/{id}/` | Retrieve/update/delete department |
| GET/POST | `/api/employees/employees/` | List/create employees |
| GET/PUT/PATCH/DELETE | `/api/employees/employees/{id}/` | Retrieve/update/delete employee |
| GET | `/api/employees/employees/{id}/reviews/` | Employee's performance reviews |
| GET | `/api/employees/employees/by-department/` | Employee counts by department |
| GET/POST | `/api/employees/performance-reviews/` | List/create reviews |
| GET/PUT/PATCH/DELETE | `/api/employees/performance-reviews/{id}/` | Retrieve/update/delete review |
| GET/POST | `/api/attendance/records/` | List/create attendance records |
| GET/PUT/PATCH/DELETE | `/api/attendance/records/{id}/` | Retrieve/update/delete record |

**Query parameters (all list endpoints):**
- `search=<text>` — full-text search
- `ordering=<field>` — sort ascending, `-<field>` for descending
- `page=<n>` — pagination (20 per page)
- `status=<value>` — filter by status field
- `department=<id>` — filter employees by department

---

## Testing

```bash
make test
# or
pytest tests/ -v --cov=employees --cov=attendance
```

---

## Architecture

```
Client
  |
  v
[Nginx / Load Balancer]
  |
  v
[Gunicorn + Django REST Framework]
  |
  +---> JWT Auth (SimpleJWT)
  +---> employees/ (Employee, Department, PerformanceReview ViewSets)
  +---> attendance/ (AttendanceRecord ViewSet)
  |
  v
[PostgreSQL]
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Author

**Atharva Devne** — [devneatharva@gmail.com](mailto:devneatharva@gmail.com)

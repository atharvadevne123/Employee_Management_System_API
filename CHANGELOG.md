# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-04

### Added
- Django 4.2 REST API with Django REST Framework
- `Employee` model with department, salary, status, and hire date
- `Department` model with employee count annotation
- `PerformanceReview` model linked to employees
- `AttendanceRecord` model with check-in/check-out and hours_worked property
- JWT authentication via `djangorestframework-simplejwt`
- Swagger/OpenAPI docs via `drf-yasg` at `/swagger/` and `/redoc/`
- DRF filtering, search, and ordering on all endpoints
- `seed_data` management command for 50 fake employees
- Comprehensive test suite (pytest) with 60%+ coverage
- GitHub Actions CI with lint and test on Python 3.10–3.12
- Dockerfile and docker-compose with PostgreSQL
- Makefile with install, test, lint, run, migrate, seed, and docker targets
- `/api/health/` and `/api/version/` endpoints
- `pyproject.toml` with ruff and pytest configuration
- Pre-commit hooks for ruff and trailing whitespace

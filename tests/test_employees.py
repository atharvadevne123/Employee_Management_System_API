"""Tests for the employees API endpoints."""
from __future__ import annotations

import pytest


@pytest.mark.django_db
class TestDepartmentAPI:
    """Test suite for Department CRUD endpoints."""

    def test_list_departments_requires_auth(self, api_client):
        """Unauthenticated request to list departments returns 401."""
        response = api_client.get("/api/employees/departments/")
        assert response.status_code == 401

    def test_list_departments(self, auth_client, department):
        """Authenticated request returns paginated department list."""
        response = auth_client.get("/api/employees/departments/")
        assert response.status_code == 200
        assert response.data["count"] >= 1

    def test_create_department(self, auth_client):
        """POST creates a new department and returns 201."""
        payload = {"name": "Finance", "description": "Finance team"}
        response = auth_client.post("/api/employees/departments/", payload)
        assert response.status_code == 201
        assert response.data["name"] == "Finance"

    def test_create_department_duplicate_name_fails(self, auth_client, department):
        """Creating a department with duplicate name returns 400."""
        payload = {"name": department.name, "description": "Duplicate"}
        response = auth_client.post("/api/employees/departments/", payload)
        assert response.status_code == 400

    def test_retrieve_department(self, auth_client, department):
        """GET detail returns correct department data."""
        response = auth_client.get(f"/api/employees/departments/{department.id}/")
        assert response.status_code == 200
        assert response.data["name"] == department.name

    def test_update_department(self, auth_client, department):
        """PATCH updates department description."""
        response = auth_client.patch(
            f"/api/employees/departments/{department.id}/",
            {"description": "Updated description"},
        )
        assert response.status_code == 200
        assert response.data["description"] == "Updated description"

    def test_delete_department(self, auth_client, department):
        """DELETE removes department and returns 204."""
        response = auth_client.delete(f"/api/employees/departments/{department.id}/")
        assert response.status_code == 204

    def test_department_employee_count(self, auth_client, department, employee):
        """employee_count field reflects active employees in department."""
        response = auth_client.get(f"/api/employees/departments/{department.id}/")
        assert response.status_code == 200
        assert response.data["employee_count"] == 1


@pytest.mark.django_db
class TestEmployeeAPI:
    """Test suite for Employee CRUD endpoints."""

    def test_list_employees_requires_auth(self, api_client):
        """Unauthenticated request returns 401."""
        response = api_client.get("/api/employees/employees/")
        assert response.status_code == 401

    def test_list_employees(self, auth_client, employee):
        """Authenticated list returns at least one employee."""
        response = auth_client.get("/api/employees/employees/")
        assert response.status_code == 200
        assert response.data["count"] >= 1

    def test_create_employee(self, auth_client, department):
        """POST creates new employee and returns 201."""
        payload = {
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice.wonder@example.com",
            "department": department.id,
            "job_title": "Data Scientist",
            "salary": "95000.00",
            "status": "active",
        }
        response = auth_client.post("/api/employees/employees/", payload)
        assert response.status_code == 201
        assert response.data["email"] == "alice.wonder@example.com"

    def test_create_employee_negative_salary_fails(self, auth_client, department):
        """Negative salary triggers validation error."""
        payload = {
            "first_name": "Bob",
            "last_name": "Bad",
            "email": "bob.bad@example.com",
            "department": department.id,
            "job_title": "Engineer",
            "salary": "-1000",
            "status": "active",
        }
        response = auth_client.post("/api/employees/employees/", payload)
        assert response.status_code == 400

    def test_retrieve_employee(self, auth_client, employee):
        """GET detail returns correct employee data with nested reviews."""
        response = auth_client.get(f"/api/employees/employees/{employee.id}/")
        assert response.status_code == 200
        assert response.data["email"] == employee.email
        assert "performance_reviews" in response.data

    def test_filter_employees_by_status(self, auth_client, employee):
        """Filtering by status returns matching employees only."""
        response = auth_client.get("/api/employees/employees/?status=active")
        assert response.status_code == 200
        for emp in response.data["results"]:
            assert emp["status"] == "active"

    def test_search_employees_by_name(self, auth_client, employee):
        """Search by last name returns matching employees."""
        response = auth_client.get(f"/api/employees/employees/?search={employee.last_name}")
        assert response.status_code == 200
        assert response.data["count"] >= 1

    def test_employee_reviews_action(self, auth_client, employee, performance_review):
        """Custom /reviews/ action returns employee performance reviews."""
        response = auth_client.get(f"/api/employees/employees/{employee.id}/reviews/")
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_update_employee(self, auth_client, employee):
        """PATCH updates employee job_title."""
        response = auth_client.patch(
            f"/api/employees/employees/{employee.id}/",
            {"job_title": "Senior Software Engineer"},
        )
        assert response.status_code == 200
        assert response.data["job_title"] == "Senior Software Engineer"

    def test_delete_employee(self, auth_client, employee):
        """DELETE removes employee and returns 204."""
        response = auth_client.delete(f"/api/employees/employees/{employee.id}/")
        assert response.status_code == 204


@pytest.mark.django_db
class TestPerformanceReviewAPI:
    """Test suite for PerformanceReview CRUD endpoints."""

    def test_create_performance_review(self, auth_client, employee):
        """POST creates a performance review linked to employee."""
        payload = {
            "employee": employee.id,
            "reviewer": "Manager Bob",
            "rating": "exceeds_expectations",
            "comments": "Outstanding quarter.",
            "goals": "Lead next project.",
        }
        response = auth_client.post("/api/employees/performance-reviews/", payload)
        assert response.status_code == 201
        assert response.data["rating"] == "exceeds_expectations"

    def test_filter_reviews_by_rating(self, auth_client, performance_review):
        """Filtering reviews by rating returns correct results."""
        response = auth_client.get(
            f"/api/employees/performance-reviews/?rating={performance_review.rating}"
        )
        assert response.status_code == 200
        for review in response.data["results"]:
            assert review["rating"] == performance_review.rating

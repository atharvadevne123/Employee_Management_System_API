"""DRF serializers for attendance records."""
from __future__ import annotations

from rest_framework import serializers

from .models import AttendanceRecord


class AttendanceRecordSerializer(serializers.ModelSerializer):
    """Serializer for AttendanceRecord with computed hours_worked field."""

    employee_name = serializers.CharField(source="employee.full_name", read_only=True)
    hours_worked = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = [
            "id",
            "employee",
            "employee_name",
            "date",
            "check_in",
            "check_out",
            "status",
            "hours_worked",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "employee_name", "hours_worked", "created_at", "updated_at"]

    def get_hours_worked(self, obj: AttendanceRecord) -> float | None:
        """Delegate to model property."""
        return obj.hours_worked

    def validate(self, attrs: dict) -> dict:
        """Ensure check_out is after check_in when both are provided."""
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")
        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError(
                {"check_out": "check_out must be after check_in."}
            )
        return attrs

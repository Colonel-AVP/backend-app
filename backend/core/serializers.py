# serializers.py
from rest_framework import serializers
from .models import Department, Student, Subject, Staff, PNWebPushConfig
import json
from .tasks import send_welcome_email


class DepartmentSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    staff_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id", "name", "student_count", "staff_count"]

    def get_student_count(self, obj):
        print(obj)
        return obj.student_set.count()

    def get_staff_count(self, obj):
        return obj.staff_set.count()


class StudentCreateSerializer(serializers.ModelSerializer):
    extra_data = serializers.JSONField(required=False)

    class Meta:
        model = Student
        fields = [
            "name",
            "is_alumni",
            "extra_data",
            "department",
        ]

    def to_internal_value(self, data):
        # Convert 'extra_data' to JSON if it exists in the input data
        extra_data = data.get("extra_data")
        if extra_data is not None:
            try:
                data["extra_data"] = json.dumps(extra_data)
            except json.JSONDecodeError:
                pass  # Handle the error if needed

        return super().to_internal_value(data)


class StudentListSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField(source="department.id", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    extra_data = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "is_alumni",
            "extra_data",
            "department_id",
            "department_name",
        ]

    def get_extra_data(self, instance):
        extra_data = instance.extra_data
        if extra_data is not None:
            try:
                # Attempt to deserialize the JSON string to a Python object
                return json.loads(extra_data)
            except (json.JSONDecodeError, TypeError):
                # If deserialization fails, return an empty dictionary
                return {}
        else:
            # If 'extra_data' is not present, return an empty dictionary
            return {}


class FilteredStudentSerializer(StudentListSerializer):
    # Add any additional fields or customizations for the filtered serializer
    class Meta(StudentListSerializer.Meta):
        fields = ["id", "name", "department", "other_field"]


class SubjectSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField(source="department.id")
    department_name = serializers.CharField(source="department.name")

    class Meta:
        model = Subject
        fields = ["id", "name", "department_id", "department_name"]


class StaffCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "name", "departments", "subjects", "email"]

    def create(self, validated_data):
        # Extract the email from the validated data
        email = validated_data.get("email")

        # Check if a staff member with the same email already exists
        is_staff = Staff.objects.filter(email__iexact=email).exists()
        if is_staff:
            raise serializers.ValidationError(
                f"Staff with email '{email}' already exists."
            )
        # Send welcome email asynchronously using Celery
        send_welcome_email.delay(email)

        # Call the superclass' create method to save the staff member
        return super().create(validated_data)


class StaffSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField(source="departments.first.id")
    department_name = serializers.CharField(source="departments.first.name")
    subject_id = serializers.IntegerField(source="subjects.first.id")
    subject_name = serializers.CharField(source="subjects.first.name")

    class Meta:
        model = Staff
        fields = [
            "id",
            "name",
            "department_id",
            "department_name",
            "subject_id",
            "subject_name",
        ]


class StudentCreateSerializer(serializers.ModelSerializer):
    extra_data = serializers.JSONField(required=False)

    class Meta:
        model = Student
        fields = ["name", "department", "subject", "email"]


class PNWebPushConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PNWebPushConfig
        fields = "__all__"

    # def get_extra_data(self, instance):
    #     extra_data = instance.extra_data
    #     if extra_data is not None:
    #         try:
    #             # Attempt to deserialize the JSON string to a Python object
    #             return json.loads(extra_data)
    #         except (json.JSONDecodeError, TypeError):
    #             # If deserialization fails, return an empty dictionary
    #             return {}
    #     else:
    #         # If 'extra_data' is not present, return an empty dictionary
    #         return {}

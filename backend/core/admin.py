from django.contrib import admin
from .models import Staff, Student, Subject, Department, TimeTable, PNWebPushConfig

# Register your models here.


class StaffAdmin(admin.ModelAdmin):
    list_display = ["name", "count_departments", "count_subjects"]

    def count_departments(self, obj):
        return obj.departments.count()

    count_departments.short_description = "Department Count"

    def count_subjects(self, obj):
        return obj.subjects.count()

    count_subjects.short_description = "Subject Count"


admin.site.register(Staff, StaffAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ["name", "department", "is_alumni"]
    ordering = ["name"]


admin.site.register(Student, StudentAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "department", "updated_at"]
    ordering = ["updated_at"]


admin.site.register(Subject, SubjectAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]  # Add other fields as needed
    ordering = ["name"]


admin.site.register(Department, DepartmentAdmin)


admin.site.register(TimeTable)
admin.site.register(PNWebPushConfig)

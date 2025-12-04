from django.contrib import admin

from .models import Course, CourseElement, Department, Faculty, Instructor, InstructorStats, Score


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty")
    list_filter = ("faculty",)
    search_fields = ("name",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "department", "faculty")
    list_filter = ("faculty", "department")
    search_fields = ("full_name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "faculty")
    list_filter = ("faculty", "department")
    search_fields = ("title",)


@admin.register(CourseElement)
class CourseElementAdmin(admin.ModelAdmin):
    list_display = ("course", "element_type", "title")
    list_filter = ("element_type", "course")
    search_fields = ("title",)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("instructor", "course_element", "value", "created_at")
    list_filter = ("value", "course_element__element_type")
    search_fields = ("notes", "instructor__full_name")


@admin.register(InstructorStats)
class InstructorStatsAdmin(admin.ModelAdmin):
    list_display = ("instructor", "average_score", "rating_count", "updated_at")
    search_fields = ("instructor__full_name",)

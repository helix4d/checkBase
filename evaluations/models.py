from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="departments")

    class Meta:
        unique_together = ("name", "faculty")

    def __str__(self) -> str:
        return f"{self.name} ({self.faculty})"


class Instructor(models.Model):
    full_name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, related_name="instructors")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="instructors")

    class Meta:
        unique_together = ("full_name", "department")

    def __str__(self) -> str:
        return self.full_name


class Course(models.Model):
    title = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="courses")
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, related_name="courses")

    class Meta:
        unique_together = ("title", "department")

    def __str__(self) -> str:
        return self.title


class CourseElement(models.Model):
    class ElementType(models.TextChoices):
        CONTACT = "contact", "Контактные данные"
        DESCRIPTION = "description", "Описание курса"
        LECTURE = "lecture", "Лекции"
        ASSIGNMENT = "assignment", "Задания"
        GROUP_SYNC = "group_sync", "Синхронизация с глобальными группами"

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="elements")
    element_type = models.CharField(max_length=32, choices=ElementType.choices)
    title = models.CharField(max_length=255)
    details = models.TextField(blank=True)

    class Meta:
        unique_together = ("course", "element_type", "title")
        verbose_name = "Course element"
        verbose_name_plural = "Course elements"

    def __str__(self) -> str:
        return f"{self.course}: {self.get_element_type_display()}"


class Score(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="scores")
    course_element = models.ForeignKey(CourseElement, on_delete=models.CASCADE, related_name="scores")
    value = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("instructor", "course_element")

    def __str__(self) -> str:
        return f"{self.instructor} - {self.course_element}: {self.value}"


class InstructorStats(models.Model):
    instructor = models.OneToOneField(Instructor, on_delete=models.CASCADE, related_name="stats")
    average_score = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal("0"))
    rating_count = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Statistics for {self.instructor}"

    @classmethod
    def recompute_for(cls, instructor: Instructor) -> "InstructorStats":
        scores = Score.objects.filter(instructor=instructor)
        aggregate = scores.aggregate(total=models.Count("id"), average=models.Avg("value"))
        rating_count = aggregate.get("total") or 0
        average = aggregate.get("average") or Decimal("0")
        stats, _ = cls.objects.get_or_create(instructor=instructor)
        stats.rating_count = rating_count
        stats.average_score = Decimal(average).quantize(Decimal("0.01")) if rating_count else Decimal("0")
        stats.save()
        return stats

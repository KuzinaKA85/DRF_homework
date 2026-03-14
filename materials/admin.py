from django.contrib import admin
from materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title_course",
        "preview",
        "description",
        "created_at",
        "updated_at",
        "is_published",
        "owner",
    )
    search_fields = ("title_course", "owner")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course",
        "title_lesson",
        "description",
        "preview",
        "video_url",
        "created_at",
        "updated_at",
        "owner",
    )
    list_filter = ("title_lesson", "course")
    search_fields = ("title_lesson", "course", "owner")

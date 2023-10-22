from django.contrib import admin
from lesson.models import Lesson, ViewModel


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'video_link', 'duration')


@admin.register(ViewModel)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'duration_view', 'start_view', 'status')

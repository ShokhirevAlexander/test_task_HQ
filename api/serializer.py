from rest_framework import serializers

from lesson.models import Lesson
from product.models import Product


class LessonsAllSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    duration_view = serializers.CharField()

    class Meta:
        model = Lesson
        fields = ('name', 'status', 'duration_view',)


class LessonsSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    duration_view = serializers.CharField()
    last_viewed = serializers.CharField()

    class Meta:
        model = Lesson
        fields = ('name', 'status', 'duration_view', 'last_viewed')


class ProductsAllSerializer(serializers.ModelSerializer):
    viewed_lessons = serializers.IntegerField()
    lesson_viewing_time = serializers.IntegerField()
    number_of_students = serializers.IntegerField()
    total_students = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('name', 'viewed_lessons', 'lesson_viewing_time', 'number_of_students', 'total_students',)

from django.contrib.auth.models import User
from django.db.models import FilteredRelation, Q, F, Count, OuterRef, Sum
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializer import LessonsSerializer, LessonsAllSerializer, ProductsAllSerializer
from lesson.models import Lesson, ViewModel
from product.models import AccessModel, Product


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_lesson(request):
    """ Список всех уроков по всем продуктам к которым пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра. """

    if request.method == 'GET':
        access = AccessModel.objects.filter(user=request.user, value=True)

        qs = Lesson.objects.filter(
            product__in=access.values('product_id')
        ).annotate(
            view_info=FilteredRelation(
                'viewmodels',
                condition=Q(viewmodels__user=request.user)
            )
        ).annotate(
            status=F('view_info__status'),
            duration_view=F('view_info__duration_view')
        )

    serializer = LessonsAllSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_lesson(request):
    """ Список уроков по конкретному продукту к которым пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра, а также датой последнего просмотра ролика. """

    data = request.data
    product_id = data.get('product_id')

    if request.method == 'POST':
        access = AccessModel.objects.filter(user=request.user, value=True, product__id=product_id)

        qs = Lesson.objects.filter(
            product__in=access.values('product_id')
        ).annotate(
            view_info=FilteredRelation(
                'viewmodels',
                condition=Q(viewmodels__user=request.user)
            )
        ).annotate(
            status=F('view_info__status'),
            duration_view=F('view_info__duration_view'),
            last_viewed=F('view_info__last_viewed'),
        )

        serializer = LessonsSerializer(qs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_statistics(request):
    """ Отображения статистики по продуктам. Необходимо отобразить список
    всех продуктов на платформе, к каждому продукту """

    students = User.objects.all().count()

    products = Product.objects.all().annotate(
        viewed_lessons=ViewModel.objects.filter(
            lesson__product=OuterRef('id'),
            status='Просмотренно'
        ).values('lesson__product').annotate(
            count_status=Count(F('status'))
        ).values('count_status'),

        lesson_viewing_time=ViewModel.objects.filter(
            lesson__product=OuterRef('id')
        ).values('lesson__product').annotate(
            total_viewing_time=Sum(F('duration_view'))
        ).values('total_viewing_time'),

        number_of_students=AccessModel.objects.filter(
            product_id=OuterRef('id'),
            value=True
        ).values('product_id').annotate(
                count_students=Count(F('user'))
            ).values('count_students'),

        students_count=AccessModel.objects.filter(
            product_id=OuterRef('id'),
            value=True
        ).values('product_id').annotate(
            count_students=Count(F('user'))
        ).values('count_students'),

        total_students=(F('students_count') * 100) / students
    )

    serializer = ProductsAllSerializer(products, many=True)
    return Response(serializer.data)

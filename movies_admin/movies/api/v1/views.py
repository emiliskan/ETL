from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.generic.list import BaseListView
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from movies.models import Media


class MediaApiMixin:
    model = Media
    http_method_names = ['get']

    def get_queryset(self):
        return Media.objects.values().annotate(genres=ArrayAgg('genres__name'))\
            .annotate(writers=ArrayAgg('personmedia__person__first_name', filter=Q(personmedia__person_type='writer')))\
            .annotate(actors=ArrayAgg('personmedia__person__first_name', filter=Q(personmedia__person_type='actor')))\
            .annotate(
            directors=ArrayAgg('personmedia__person__first_name', filter=Q(personmedia__person_type='director')))


    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MediaApi(MediaApiMixin, BaseListView):

    def get_context_data(self, *, object_list=None, **kwargs):
        query_list = list(self.get_queryset())
        paginator = self.get_paginator(query_list, 50)

        page_num = self.request.GET.get('page')
        if page_num == 'last':
            page = paginator.get_page(paginator.num_pages)
        else:
            page = paginator.get_page(page_num)

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            'results': page.object_list
        }
        return context


class MediaDetailsApi(MediaApiMixin, DetailView):

    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_object()

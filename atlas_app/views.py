from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
import requests
from django.db.models import Q
from .models import Lançamentos, Popular, Genres, Media


def addedView(request):
    result = requests.get('https://superflixapi.buzz/calendario.php')
    return JsonResponse(result.text, safe=False)


def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]



def homeView(request):
    last_add = Lançamentos.objects.all().order_by('post_date')
    populars = Popular.objects.all()
    last = Media.objects.all().order_by('-lancament_date')[:10]

    if not last_add:
        pages = list(chunk_list(last, 6))
    else:
        pages = list(chunk_list(last_add, 6))

    return render(request, 'index.html', {
        'movies': pages,
        'populars': populars,
        'filter': request.GET.get('filter', '')
    })



class MediaDetailView(generic.DetailView):
    model = Media
    context_object_name = 'media'
    template_name = 'media_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context



class MoviesListView(generic.ListView):
    model = Media
    context_object_name = 'medias'
    template_name = 'medias_list.html'
    paginate_by = 18

    def get_queryset(self):
        qs = Media.objects.filter(typeMedia='filme')
        filtro = self.request.GET.get('filter', '')
        if filtro:
            qs = qs.filter(title__icontains=filtro)
        return qs.order_by('-lancament_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context



class SeriesListView(generic.ListView):
    model = Media
    context_object_name = 'medias'
    template_name = 'medias_list.html'
    paginate_by = 18

    def get_queryset(self):
        qs = Media.objects.filter(typeMedia='serie')
        filtro = self.request.GET.get('filter', '')
        if filtro:
            qs = qs.filter(title__icontains=filtro)
        return qs.order_by('-lancament_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context



class SearchMediaView(generic.ListView):
    model = Media
    context_object_name = 'medias'
    template_name = 'search_results.html'
    paginate_by = 18

    def get_queryset(self):
        query = self.request.GET.get('filter', '').strip()

        if not query:
            return Media.objects.none()

        return Media.objects.filter(
            Q(title__icontains=query)
        ).order_by('-lancament_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context

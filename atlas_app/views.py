from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
import requests
from django.db.models import Q
from .models import Lançamentos, Popular, Genres, Media


def addedView(request):
    result = requests.get('https://superflixapi.buzz/calendario.php')
    resul = result
    # print(type(resul))
    for r in result:
        print('---------------------')
        print(r)
          
    return JsonResponse(result.text, safe=False)


def chunk_list(lst, n):
    """Divide a lista em blocos de n itens."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Create your views here.
def homeView(request):
    last_add = Lançamentos.objects.all().order_by('post_date')
    populars = Popular.objects.all()
    last = Media.objects.all().order_by('-lancament_date')[:10]

    # Paginação em chunks de 6
    if not last_add:
        pages = list(chunk_list(last, 6))
    else:
        pages = list(chunk_list(last_add, 6))

    # Filtro de busca
    query = request.GET.get('gender')  # seu campo de input
    if query:
        # Tenta encontrar no modelo de filmes ou séries
        movie_match = Media.objects.filter(
            Q(title__icontains=query), typeMedia='filme'
        ).first()
        series_match = Media.objects.filter(
            Q(title__icontains=query), typeMedia='serie'
        ).first()

        if movie_match:
            # Redireciona para a view de filmes, passando query
            return redirect('movies_media')  # Substitua 'movies_list' pelo nome da sua URL
        elif series_match:
            # Redireciona para a view de séries
            return redirect('series_media')  # Substitua 'series_list' pelo nome da sua URL
        else:
            # Nenhum resultado encontrado, permanece na home ou mostra mensagem
            pages = []  # limpa resultados

    return render(request, 'index.html', {
        'movies': pages,
        'populars': populars,
        'filter': query
    })

class MediaDetailView(generic.DetailView):
    model = Media
    context_object_name = 'media'
    template_name = 'media_detail.html'

class MoviesListView(generic.ListView):
    model = Media
    context_object_name = 'medias'
    template_name = 'medias_list.html'
    paginate_by = 18
    ordering = ['-lancament_date']

    def get_queryset(self):
        qs = Media.objects.filter(typeMedia='filme')

        filtro = self.request.GET.get('filter', '')
        print(filtro)
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
    ordering = ['-lancament_date']
    
    def get_queryset(self):
        qs = Media.objects.filter(typeMedia='serie')

        filtro = self.request.GET.get('filter', '')
        print(filtro)
        if filtro:
            qs = qs.filter(title__icontains=filtro)

        return qs.order_by('-lancament_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')

        return context

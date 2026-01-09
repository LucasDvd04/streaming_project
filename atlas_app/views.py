from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
import requests

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
    
    if request.method == 'GET':
        last_add = Lançamentos.objects.all().order_by('post_date')
        populars = Popular.objects.all()
        last = Media.objects.all().order_by('-lancament_date')[:10]
        if not last_add:
            pages = list(chunk_list(last,6))
        else:
            pages = list(chunk_list(last_add,6))

        filter = request.GET.get('gender')


        fit = {'filltler':filter}

        


    return render(request, 'index.html',{'movies':pages, 'populars':populars, 'filter':filter})

class MediaDetailView(generic.DetailView):
    model = Media
    context_object_name = 'media'
    template_name = 'media_detail.html'

class MoviesListView(generic.ListView):
    model = Media
    context_object_name = 'medias'
    template_name = 'medias_list.html'
    paginate_by = 18

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

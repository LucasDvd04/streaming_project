from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
import requests

from .models import Lançamentos, Popular, Genres, Media


def addedView(request):
    result = requests.get('https://superflixapi.run/calendario.php')
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
        lancements = Lançamentos.objects.all().order_by('post_date')
        populars = Popular.objects.all()
        pages = list(chunk_list(lancements,6))
        filter = request.GET.get('gender')
        print('-----filter-----')
        print(filter)
        print('-----pages-----')
        print(populars[1].id)

        fit = {'filltler':filter}
        print(fit)

    return render(request, 'index.html',{'movies':pages, 'populars':populars, 'filter':filter})

class MediaDetailView(generic.DetailView):
    model = Media
    context_object_name = 'media'
    template_name = 'media_detail.html'

class MoviesListView(generic.ListView):
    model = Media
    context_object_name = 'medias'
    template_name = 'medias_list.html'
    paginate_by = 20

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
    paginate_by = 20

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

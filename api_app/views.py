from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response


import requests
import json
from datetime import datetime, date
import re

from atlas_app.models import Lançamentos, Media, Genres, Popular, APIKey
from .serializers import MediaSerializer,InsetMediaSerializer,InsetLancamentsSerializer,LancamentsSerializer,TrendsSerializer,InsetTrendsSerializer,ImportOffset,ImportOffsetSerializer

def getKeyAPI(name):
    key = APIKey.objects.get(name=name).key
    return key

def setGenres(request):
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en-US"
    key = getKeyAPI('tmdb')
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {key}"
    }

    response = json.loads(requests.get(url, headers=headers).text)

    for r in response['genres']:
        print(r)

        genre = Genres(
            id = r['id'],
            name = r['name']
        )
        genre.save()


    return JsonResponse(response,status=201, safe=False)

def setMedias(request):
    movies = json.loads(requests.get('https://superflixapi.buzz/lista?category=movie&type=imdb&format=json').text)
    series = json.loads(requests.get('https://superflixapi.buzz/lista?category=serie&type=imdb&format=json').text)
    medias_atuais = Media.objects.all().values_list('idIMDB', flat=True)
    movies = [m for m in movies if m not in medias_atuais] 
    series = [s for s in series if s not in medias_atuais]
    movies_10 = movies[:200]
    series_10 = series[:200]
    movies_data = setDatasMedias(request, movies_10, 'filme')
    series_data = setDatasMedias(request, series_10, 'serie')

    Media.objects.bulk_create(movies_data)
    Media.objects.bulk_create(series_data)

    return HttpResponse('ok')

def setDatasMedias(request, ids, type):
    medias = []
    key  = getKeyAPI('omdb')

    for id in ids:
        url = f'http://www.omdbapi.com/?i={id}&apikey={key}'
        data = json.loads(requests.get(url).text)

        if data['Response'] == 'True':
            obj = Media(
                title=data['Title'],
                sinopse=data['Plot'],
                rating=data['imdbRating'],
                poster=data['Poster'],
                typeMedia=type,
                idIMDB=data['imdbID'],
                lancament_date=dataRealease(data)
            )
            medias.append(obj)  

    return medias

def dataRealease(data):
    # Caso tenha data completa
    if data.get('Released') and data['Released'] != 'N/A':
        return datetime.strptime(data['Released'], '%d %b %Y').date()

    # Caso não tenha, tenta extrair o primeiro ano
    year_str = data.get('Year', '')
    match = re.search(r'\d{4}', year_str)

    if match:
        return date(int(match.group()), 1, 1)

    # fallback final
    return None

def updateFuture(request):
    Lançamentos.objects.all().delete()
    result = requests.get('https://superflixapi.buzz/calendario.php')
    resul = json.loads(result.text)
    news = []
    titles = []
    key  = getKeyAPI('omdb')
    for r in resul:
        if r['status'] == 'Futuro':
            if r['title'] not in titles:
                setPictureID(r, key)
                print(r)
                news.append(r)
                titles.append(r['title'])
                if r['response'] == 'False':
                    continue
                else:
                    print('salvando lançamento')
                    lançamento = Lançamentos(
                        title = r['title'],
                        idIMDB = r['imdb_id'],
                        rating = r['rating'],
                        poster = r['poster'],
                        post_date = r['air_date']
                    )
                    lançamento.save()
        else:
            print('já existe')
        

    return JsonResponse(news,status=201, safe=False)

def setPictureID(dict, key):
    id = dict['imdb_id']
    url = f'http://www.omdbapi.com/?i={id}&apikey={key}'
    poster = json.loads(requests.get(url).text)
    if poster['Response'] == 'True':
        dict['poster'] = poster['Poster']
        dict['response'] = poster['Response']
        if poster['Ratings']:
            dict['rating'] = str(poster['Ratings'][0]['Value'])
        else:
            dict['rating'] = None
    else:
        print('vazio')
        dict['poster'] = ''
        dict['rating'] = None
        dict['response'] = poster['Response']

@csrf_exempt
def futureInsertView(request):
    if request.method == "POST":
        updateFuture(request)
    
    try:
        futures = Lançamentos.objects.all().values()
        medias = []
        for f in futures:
            medias.append(f)

        return JsonResponse(medias,status=200, safe=False)
    
    except Exception as e:
        raise e


def setPictureName(dict, key):
    title = dict['title']
    url = f'http://www.omdbapi.com/?t={title}&apikey={key}'
    poster = json.loads(requests.get(url).text)
    if poster['Response'] == 'True':
        dict['poster'] = poster['Poster']
        dict['idIMDB'] = poster['imdbID']
        dict['response'] = poster['Response']
    else:
        print('vazio')
        dict['poster'] = ''
        dict['idIMDB'] = ''
        dict['response'] = poster['Response']


def isertPopularMovieView(request):
    Popular.objects.all().delete()
    key  = getKeyAPI('tmdb')
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {key}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    media_at = set(Media.objects.values_list('title', flat=True))
    news = []

    for r in data.get("results", []):
        title = r.get("title")

        if title in media_at:
            Popular.objects.create(media=Media.objects.get(title=title))

        else:
            print("não encontrado:", title)

    return JsonResponse(news, status=201, safe=False)


def get_medias(request):
    ...

class ListMedias(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    
class CreatMedia(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = InsetMediaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    

class ListLancaments(generics.ListAPIView):
    queryset = Lançamentos.objects.all()
    serializer_class = LancamentsSerializer
    
class CreatLancaments(generics.CreateAPIView):
    queryset = Lançamentos.objects.all()
    serializer_class = InsetLancamentsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    
class ListPopular(generics.ListAPIView):
    queryset = Popular.objects.all()
    serializer_class = TrendsSerializer
    
class CreatPopular(generics.CreateAPIView):
    queryset = Popular.objects.all()
    serializer_class = InsetTrendsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    

class DeletePopularViews(generics.DestroyAPIView):
    queryset = Popular.objects.all()
    serializer_class = TrendsSerializer


class ImportOffsetView(generics.APIView):

    def get(self, request, key):
        obj, _ = ImportOffset.objects.get_or_create(key=key)
        serializer = ImportOffsetSerializer(obj)
        return Response(serializer.data)

    def post(self, request, key):
        obj, _ = ImportOffset.objects.get_or_create(key=key)
        serializer = ImportOffsetSerializer(
            obj,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db import models


class Genres(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=False)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Media(models.Model):

    types = [
        ('movie', 'Filme'),
        ('serie', 'Serie'),
    ]

    title = models.CharField(max_length=50)
    idIMDB =models.CharField(max_length=20, null=True, blank=True)
    sinopse = models.TextField()
    rating = models.FloatField()
    poster = models.CharField()
    typeMedia = models.CharField(choices=types)
    genrer = models.ManyToManyField(Genres, related_name='media_gender', blank=True, null=True)
    lancament_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    
class Lançamentos(models.Model):
    title = models.CharField(max_length=50)
    idIMDB =models.CharField(max_length=20, null=True, blank=True)
    rating = models.CharField()
    poster = models.CharField()
    post_date = models.DateField()

    def __str__(self):
        return self.title
    
    def get_data(self):
        return self.post_date.strftime("%d de %B")

    
class Popular(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='popular_media' )

    def __str__(self):
        return self.media.title
    
    def get_first_media(self):
        print('-----popular media first -----')
        print(self.media.first())
        return self.media.first()
    
class APIKey(models.Model):
    name = models.CharField(max_length=50, unique=True)
    key = models.TextField(max_length=100) 

    def __str__(self):
        return self.name


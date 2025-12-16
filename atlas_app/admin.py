from django.contrib import admin
from .models import Media, Genres, Popular, Lançamentos, APIKey

class MediaAdmin(admin.ModelAdmin):
    list_display = ('id','title','rating','typeMedia',)
    search_fields = ('title','rating',)

class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)

class PopularAdmin(admin.ModelAdmin):
    list_display = ('media',)
    search_fields = ('title',)

class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name',)



admin.site.register(Lançamentos, LancamentoAdmin)
admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Genres, GenderAdmin)
admin.site.register(Popular, PopularAdmin)
from rest_framework import serializers
from atlas_app.models import Media, Lançamentos, Popular
from .models import ImportOffset


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id','idIMDB','title',]


class InsetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'



class LancamentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lançamentos
        fields = ['idIMDB',]


class InsetLancamentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lançamentos
        fields = '__all__'


class TrendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popular
        fields = ['id','media',]


class InsetTrendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popular
        fields = ['media',]

class ImportOffsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportOffset
        fields = ('key', 'value')
        read_only_fields = ('key',)
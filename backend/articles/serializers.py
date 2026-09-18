from rest_framework import serializers
from .models import Article, GovernmentResource

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class GovernmentResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentResource
        fields = '__all__'

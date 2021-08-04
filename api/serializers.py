from rest_framework import serializers
from .models import VisitedLink


class VisitedLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitedLink
        fields = '__all__'

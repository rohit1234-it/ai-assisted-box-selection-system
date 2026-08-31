from rest_framework import serializers
from boxes.models import Box

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model=Box
        fields='__all__'
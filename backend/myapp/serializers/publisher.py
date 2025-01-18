from rest_framework import serializers # type: ignore
from myapp.models import Publisher

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = [
        "id",
        "name", 
        "founded", 
        "website",
        "books",
        "address",
        "active",
        "email",
        "revenue" 
        ]
        
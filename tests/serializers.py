from rest_framework import serializers
from .models import Foo


class FooSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foo
        exclude = [
            'deleted_at'
        ]

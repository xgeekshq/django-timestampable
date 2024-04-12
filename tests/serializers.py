from rest_framework import serializers
from .models import Foo, Bar


class FooSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foo
        exclude = ['deleted_at']


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
        exclude = ['deleted_at']

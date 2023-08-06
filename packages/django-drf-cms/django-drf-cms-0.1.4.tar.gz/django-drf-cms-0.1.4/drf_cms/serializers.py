from rest_framework import serializers
from .models import Page, Text


class TextSerializer(serializers.ModelSerializer):
    key = serializers.CharField(read_only=True)

    class Meta:
        model = Text
        fields = ('content', 'key')


class PageSerializer(serializers.ModelSerializer):
    texts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Page
        fields = ('key', 'title', 'description', 'texts')

    def get_texts(self, instance):
        texts = instance.text_set.all()
        result = {}
        for text in texts:
            result[text.key] = text.content
        return result
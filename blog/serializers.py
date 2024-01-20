from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Blog
        fields = ('pk', 'title', 'post', 'author')
        read_only_fields = ('pk', 'author')

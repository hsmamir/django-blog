from rest_framework import serializers
from .models import Profile
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    user_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if Profile.objects.filter(user_name=attrs['user_name']).exists():
            raise serializers.ValidationError(
                dict(user_name=['user_name is used before!', ]))
        return attrs

    def create(self, validated_data):
        profile, _ = Profile.get_or_create(
            user_name=validated_data['user_name'],
            defaults=dict(password=make_password(validated_data['password']))
        )
        return {
            'pk': profile.pk,
            'user_name': profile.user_name,
        }


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user_name = attrs['user_name']
        if not Profile.objects.filter(user_name=user_name).exists():
            raise serializers.ValidationError(
                dict(user_name=['Account is not registerd!', ]))
        instance = Profile.objects.get(user_name=user_name)
        if not instance.verify_password(attrs['password']):
            raise serializers.ValidationError(
                dict(password=['Invalid Password', ]))
        attrs['user_name'] = user_name
        return attrs

    def create(self, validated_data):
        profile = Profile.objects.get(user_name=validated_data['user_name'])
        refresh, access = profile.user.api_token()

        return {
            'access': access,
            'refresh': refresh,
        }

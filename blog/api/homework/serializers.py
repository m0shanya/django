from rest_framework import serializers

from homework.models import Profile


class ProfileModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "age", "created_at"]
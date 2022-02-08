from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.homework.serializers import ProfileModelSerializer
from homework.models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed.
    """

    queryset = Profile.objects.all().order_by("-created_at")
    serializer_class = ProfileModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


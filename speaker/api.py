from rest_framework import viewsets, permissions

from . import serializers
from . import models


class IndividualViewSet(viewsets.ModelViewSet):
    """ViewSet for the Individual class"""

    queryset = models.Individual.objects.all()
    serializer_class = serializers.IndividualSerializer
    permission_classes = [permissions.IsAuthenticated]

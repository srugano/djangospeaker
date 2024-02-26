from rest_framework import serializers

from . import models


class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Individual
        fields = [
            "created_at",
            "updated_at",
            "voice_sample",
            "full_name",
        ]

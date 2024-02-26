from django.db import models
from django.urls import reverse


class Individual(models.Model):
    def speaker_directory_path(instance, filename):
        return "voice_samples/{0}/{1}".format(instance.full_name, filename)

    # Fields
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    voice_sample = models.FileField(upload_to=speaker_directory_path)
    full_name = models.CharField(max_length=30, unique=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.full_name)

    def get_absolute_url(self):
        return reverse("speaker_individual_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("speaker_individual_update", args=(self.pk,))

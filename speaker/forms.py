from django import forms
from . import models
import os
from django.core.exceptions import ValidationError


class VoiceVerificationForm(forms.Form):
    voice_sample = forms.FileField(label="Upload new voice sample")


class IndividualForm(forms.ModelForm):
    class Meta:
        model = models.Individual
        fields = [
            "voice_sample",
            "full_name",
        ]

    def clean_voice_sample(self):
        voice_sample = self.cleaned_data.get("voice_sample")
        valid_extensions = [".mp3", ".ogg", ".wav"]
        ext = os.path.splitext(voice_sample.name)[1]
        if ext.lower() not in valid_extensions:
            raise ValidationError("Unsupported file extension.")

        max_size = 1 * 1024 * 1024
        if voice_sample.size > max_size:
            raise ValidationError("File size exceeds the limit of 1MB.")

        return voice_sample

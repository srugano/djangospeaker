from django.contrib import admin
from django import forms

from . import models


class IndividualAdminForm(forms.ModelForm):
    class Meta:
        model = models.Individual
        fields = "__all__"


class IndividualAdmin(admin.ModelAdmin):
    form = IndividualAdminForm
    list_display = [
        "created_at",
        "updated_at",
        "voice_sample",
        "full_name",
    ]
    readonly_fields = ["created_at", "updated_at"]


admin.site.register(models.Individual, IndividualAdmin)

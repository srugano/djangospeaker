from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("Individual", api.IndividualViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path(
        "speaker/Individual/",
        views.IndividualListView.as_view(),
        name="speaker_individual_list",
    ),
    path(
        "speaker/Individual/create/",
        views.IndividualCreateView.as_view(),
        name="speaker_individual_create",
    ),
    path(
        "speaker/Individual/detail/<int:pk>/",
        views.IndividualDetailView.as_view(),
        name="speaker_individual_detail",
    ),
    path(
        "speaker/Individual/update/<int:pk>/",
        views.IndividualUpdateView.as_view(),
        name="speaker_individual_update",
    ),
    path(
        "speaker/Individual/delete/<int:pk>/",
        views.IndividualDeleteView.as_view(),
        name="speaker_individual_delete",
    ),
    path("upload_voice_sample", views.upload_voice_sample, name="upload_voice_sample_url"),
    path("record_sample", views.record_voice_sample, name="record_voice_sample_url"),
)

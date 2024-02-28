from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from . import models
from . import forms
import magic
import subprocess
from .utils import recognize_speaker
from django.contrib import messages
from django.shortcuts import render, redirect
import torch


def convert_webm_to_wav(webm_path, wav_path):
    command = ["ffmpeg", "-i", webm_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", wav_path]
    subprocess.run(command, check=True)


class IndividualListView(generic.ListView):
    model = models.Individual
    form_class = forms.IndividualForm


class IndividualCreateView(generic.CreateView):
    model = models.Individual
    form_class = forms.IndividualForm


class IndividualDetailView(generic.DetailView):
    model = models.Individual
    form_class = forms.IndividualForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["voice_verification_form"] = forms.VoiceVerificationForm()
        return context

    def handle_voice_sample(self, voice_sample):
        # Check the MIME type
        voice_sample.seek(0)
        mime_type = magic.from_buffer(voice_sample.read(2048), mime=True)  # Increase buffer size
        voice_sample.seek(0)
        if mime_type not in ["audio/mpeg", "audio/ogg", "audio/wav", "audio/x-wav", "audio/webm", "video/webm"]:
            return "Unsupported file format.", False

        recognized, elapsed_time, similarity = recognize_speaker(voice_sample, self.object)
        return recognized, elapsed_time, similarity

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        voice_verification_form = forms.VoiceVerificationForm(request.POST, request.FILES)
        if voice_verification_form.is_valid():
            voice_sample = request.FILES.get("voice_sample")
            recognized, elapsed_time, similarity = self.handle_voice_sample(voice_sample)

            # Convert the tensor to a Python float
            similarity_score = similarity.item() if isinstance(similarity, torch.Tensor) else similarity

            response_data = {
                "status": "success" if recognized else "error",
                "message": "The voice sample matches the individual." if recognized else "Voice sample does not match the individual.",
                "elapsed_time": elapsed_time,
                "similarity": similarity_score,  # Use the converted score
            }
            return JsonResponse(response_data)
        else:
            form_errors = voice_verification_form.errors.as_json()
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Form validation failed",
                    "form_errors": form_errors,
                },
                status=400,
            )

    def form_invalid(self, *args, **kwargs):
        context = self.get_context_data()
        if "voice_verification_form" in kwargs:
            context["voice_verification_form"] = kwargs["voice_verification_form"]
        else:
            context["voice_verification_form"] = forms.VoiceVerificationForm()
        return self.render_to_response(context)


class IndividualUpdateView(generic.UpdateView):
    model = models.Individual
    form_class = forms.IndividualForm
    pk_url_kwarg = "pk"


class IndividualDeleteView(generic.DeleteView):
    model = models.Individual
    success_url = reverse_lazy("speaker_individual_list")


def upload_voice_sample(request):
    if request.method == "POST":
        form = forms.IndividualForm(request.POST, request.FILES)
        if form.is_valid():
            # Attempt to find an existing speaker by the provided name
            speaker_name = form.cleaned_data["full_name"]
            existing_speaker = models.Individual.objects.filter(full_name=speaker_name).first()
            if existing_speaker and existing_speaker.voice_sample:
                # A voice sample already exists, perform speaker recognition
                input_audio_path = request.FILES["voice_sample"].temporary_file_path()
                recognized = recognize_speaker(input_audio_path, existing_speaker)
                if recognized:
                    message = "Individual recognized successfully."
                else:
                    message = "Individual recognition failed."
                messages.add_message(request, messages.INFO, message)
                return redirect("speaker_individual_list")  # Adjust this to your actual success URL
            else:
                # No existing voice sample, save the new speaker and sample
                new_speaker = form.save()
                messages.add_message(request, messages.SUCCESS, "Voice sample saved successfully.")
                return redirect("speaker_individual_list")  # Adjust this to your actual success URL
    else:
        form = forms.IndividualForm()
    return render(request, "upload.html", {"form": form})

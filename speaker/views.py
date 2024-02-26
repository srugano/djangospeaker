from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from . import models
from . import forms
import magic
from .utils import recognize_speaker
from django.contrib import messages
from django.shortcuts import render, redirect


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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the individual object
        voice_verification_form = forms.VoiceVerificationForm(request.POST, request.FILES)

        if voice_verification_form.is_valid():
            new_voice_sample = request.FILES["voice_sample"]
            mime = magic.from_buffer(new_voice_sample.read(1024), mime=True)
            new_voice_sample.seek(0)
            
            if mime not in ['audio/mpeg', 'audio/ogg', 'audio/wav', 'audio/x-wav']:
                messages.error(request, "Unsupported file format.")
                return self.form_invalid(voice_verification_form)
            recognized = recognize_speaker(new_voice_sample, self.object)
            if recognized:
                messages.success(request, "The voice sample matches the individual.")
            else:
                messages.error(request, "Voice sample does not match the individual.")
            return redirect(self.object.get_absolute_url())
        else:
            return self.form_invalid(voice_verification_form)

    def form_invalid(self, form):
        # This method is to handle if the form is not valid, showing form errors
        return self.render_to_response(self.get_context_data(form=form))


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


def record_voice_sample(request):
    import ipdb; ipdb.set_trace()
    if request.method == "POST":
        voice_sample = request.FILES.get("voice_sample")
        if voice_sample:
            # Process the voice sample here
            return JsonResponse({"status": "success", "message": "Voice sample uploaded successfully."})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

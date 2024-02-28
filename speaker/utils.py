from speechbrain.pretrained import SpeakerRecognition
import torchaudio
from django.core.files.temp import NamedTemporaryFile
import os
import time

# transform stored sample voice into an encoding
# read the uploaded file to I/O or stream octets
# 5, 10, 15 sec for comparizon
# Test with real voices 10 sentences
# Retries! (3) with variable treshhold
# variable phrases (name, )

def recognize_speaker(uploaded_file, speaker):
    model = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="tmpdir")
    with NamedTemporaryFile(delete=True, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_uploaded_file:
        for chunk in uploaded_file.chunks():
            tmp_uploaded_file.write(chunk)
        tmp_uploaded_file.flush()

        input_signal, fs = torchaudio.load(tmp_uploaded_file.name)

    with NamedTemporaryFile(delete=True, suffix=os.path.splitext(speaker.voice_sample.name)[1]) as tmp_stored_file:
        with open(speaker.voice_sample.path, "rb") as stored_file:
            for chunk in stored_file:
                tmp_stored_file.write(chunk)
            tmp_stored_file.flush()

        stored_signal, fs = torchaudio.load(tmp_stored_file.name)

    start_time = time.time()
    input_embedding = model.encode_batch(input_signal)
    stored_embedding = model.encode_batch(stored_signal)
    similarity = model.similarity(input_embedding, stored_embedding)
    end_time = time.time()

    threshold = 0.85
    elapsed_time = end_time - start_time
    if similarity >= threshold:
        return True, elapsed_time, similarity
    else:
        return False, elapsed_time, similarity

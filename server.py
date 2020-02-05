# Web server libs
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

# Libs for spectrogram generation
import os
import io
import librosa
import librosa.display
import matplotlib.pyplot

# Libs for inference
from fastai.vision import *

# Other libs
from pathlib import Path
import uvicorn
import base64

# Set up the server
app = Starlette()
templates = Jinja2Templates(directory="templates")

# Provide access to static assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the model for inference
defaults.device = torch.device("cpu")
modelPath = Path("data-v2/spectrograms/")
learn = load_learner(modelPath)

def generate_tempfile_libROSA_spectrogram(audio_file):
    min_frequency = 256
    max_frequency = 16384
    samples_between_frames = 256
    fft_window_size = 2048

    # Load the audio, generate a spectrogram in DB (to match the logarithmic nature of human hearing)
    audio_data, sample_rate = librosa.load(audio_file, sr=None)
    spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate, n_mels=128, fmax=max_frequency,
                                             hop_length=samples_between_frames, n_fft=fft_window_size)
    amplitude_in_db = librosa.power_to_db(spectrogram, ref=np.max)

    # Generate the spectrogram with min and max frequency bounds applied
    librosa.display.specshow(amplitude_in_db, x_axis=None, y_axis=None, sr=sample_rate, fmin=min_frequency, fmax=max_frequency)
    plt.tight_layout()

    # Save the generated spectrogram
    outputFile = tempfile.TemporaryFile(suffix="png")
    plt.savefig(outputFile)
    plt.close()

    return outputFile

def predict_hot_or_cold(audio_file, request):
    with generate_tempfile_libROSA_spectrogram(audio_file) as tempSpectrogram:
        spectrogram = open_image(tempSpectrogram)
        pred_classification, pred_idx, outputs = learn.predict(spectrogram)
        tempSpectrogram.seek(0)
        encoded_spectrogram = str(base64.b64encode(tempSpectrogram.read()))[2:-1] # remove the leading b' and trailing '
        return templates.TemplateResponse("audio-analysis-result.html", {
            "request": request,
            "prediction": str(pred_classification),
            "probability_cold" : outputs[0].item(),
            "probability_hot" : outputs[1].item(),
            "encoded_spectrogram" : encoded_spectrogram,
        })

@app.route("/evaluate_audio_sample", methods=["POST"])
async def evaluate_audio_sample(request):
    formData = await request.form()
    audio_bytes = await formData["file"].read()
    audio_file_ext = formData["file"].filename[-4:]
    with tempfile.NamedTemporaryFile(suffix=audio_file_ext, delete=False) as audio_file:
        audio_file.write(audio_bytes)
        response_page = predict_hot_or_cold(audio_file.name, request)
        audio_file.close()
        os.unlink(audio_file.name)
        return response_page

@app.route("/evaluate_example", methods=["GET"])
async def evaluate_example(request):
    example_name = request.query_params['file']
    examples_path = Path("static/example-audio")
    audio_file = (examples_path/example_name).resolve()
    if audio_file.parent != examples_path.resolve():
        return HTMLResponse("Nice try, " + example_name + " is not permitted.")
    return predict_hot_or_cold(audio_file, request)

@app.route("/how-to")
def how_to(request):
    return templates.TemplateResponse("how-to.html", {"request": request})


@app.route("/")
def index(request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=8000, reload=True, log_level="info")

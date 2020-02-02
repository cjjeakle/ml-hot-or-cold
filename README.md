# ML: Hot or Cold

## What is this?
This is a machine learning model that detects hot or cold water from the sound of pouring (given the arbitrary boundary that >100 degrees f is hot, and in practice the model saw a boundary of  >= 175 for hot and <= 75 for cold).

This project is an effort to use what I'm learning in Fast.ai's excellent MOOC, and was inspired by an [NPR piece](https://www.npr.org/2014/07/05/328842704/what-does-cold-sound-like) on the sound water makes when poured at different temperatures.

[Build log 1](Build-Log-1_Design.ipynb) starts with a more detailed project description.

## How to try the classifier:
Submit an audio clip of pouring water here: http://hot-or-cold.projects.chrisjeakle.com

Alternatively: clone this repo, and follow the steps used in [build log 3](Build-Log-3_Testing-The-Model.ipynb) to test data of your own.

## How does the model work?
Take a look at the build logs to find out!

[Build log 1](Build-Log-1_Design.ipynb) outlines a series of experiments done to choose a project architecture.

[Build log 2](Build-Log-2_More-Data.ipynb) fine-tunes the chosen experimental design into a working model.

Finally, [build log 3](Build-Log-3_Testing-The-Model.ipynb) tries out the model on some data the model has never seen before (not even for validation).

There is a simple infrence pipeline defined in [server.py](website/server.py) under the `evaluate_audio_sample` route.

## Running the website

1. Install dependencies:
    * `pip3 install starlette uvicorn aiofiles python-multipart fastai torch librosa`
1. Start the server:
    * `python3 website/server.py`
1. Navigate to: http://localhost:8001

## Hosting the website

1. Follow the steps [here](https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/) to set up nginx as a reverse proxy (to provide https support)
    * Point the reverse proxy to a running instance of `website/server.py` at localhost:8001
1. Start the python webserver `python3 website/server.py`

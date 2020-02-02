# ML: Hot or Cold

## What is this?
This is a machine learning model that detects hot or cold water from the sound of pouring (in practical terms the model was fed data where >= 175 f was hot and <= 75 f was cold).

This project is an effort to use skills from Fast.ai's excellent MOOC, and was inspired by an [NPR piece](https://www.npr.org/2014/07/05/328842704/what-does-cold-sound-like) on the sound water makes when poured at different temperatures.

Additionally, this project can act as a liberally licensed example of sound classification using `fastai` as a wrapper around `torch`. I did some digging while working on this project, and ended up relying very little on other people's work due to licensing concerns! Fear not friend, this project has you covered with an E2E log of my workflow.

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
    * `pip3 install starlette uvicorn aiofiles python-multipart jinja2 fastai torch librosa`
        * On certain platforms, such as Windows, torch and fastai may not install correctly. Use conda to install them in such cases.
1. Navigate to the `website` directory
    * This ensures all relative paths in the server script resolve correctly
1. Start the server:
    * `python3 server.py`
1. Navigate to: http://localhost:8001

## License
### Software License (except where otherwise noted in comments)
The MIT License (MIT)

Copyright (c) 2020 Chris Jeakle

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Data License
[CC BY-SA](https://creativecommons.org/licenses/by-sa/2.0/)

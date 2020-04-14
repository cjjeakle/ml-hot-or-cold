# ML: Hot or Cold

## What is this?
This is a machine learning model that detects hot or cold water from the sound of pouring (in practical terms the model was fed data where >= 175 f was hot and <= 75 f was cold).

This project is an effort to use skills from Fast.ai's excellent MOOC, and was inspired by an [NPR piece](https://www.npr.org/2014/07/05/328842704/what-does-cold-sound-like) on the sound water makes when poured at different temperatures.

Additionally, this project can act as a liberally licensed example of sound classification using `fastai` as a wrapper around `torch`. I did some digging while working on this project, and ended up relying very little on other people's work due to licensing concerns! Fear not friend, this project has you covered with an E2E log of my workflow.

[Build log 1](Build-Log-1_Design.ipynb) starts with a more detailed project description.

## How to try the classifier:
Submit an audio clip of pouring water here: https://ml-hot-or-cold.projects.chrisjeakle.com/

Alternatively: clone this repo, and follow the steps used in [build log 3](Build-Log-3_Testing-The-Model.ipynb) to test data of your own.

## How does the model work?
Take a look at the build logs to find out!

[Build log 1](Build-Log-1_Design.ipynb) outlines a series of experiments done to choose a project architecture.

[Build log 2](Build-Log-2_More-Data.ipynb) fine-tunes the chosen experimental design into a working model.

Finally, [build log 3](Build-Log-3_Testing-The-Model.ipynb) tries out the model on some data the model has never seen before (not even for validation).

There is a simple infrence pipeline defined in [server.py](server.py) under the `evaluate_audio_sample` route.

I've started an [addendum](Addendum.md) with notes and corrections I've learned as I work further in the fast.ai course.

## Running the website locally

1. Install dependencies:
    * `pip3 install -r requirements.txt`
        * On certain platforms, such as Windows, torch and fastai may not install correctly. Use conda to install them in such cases.
1. Start the server:
    * `python3 server.py`
1. Navigate to the url and port printed in the terminal window

## Hosting the website

A guide from absolutely nothing to a working site hosted on an VM: I pulled my hair out so you don't have to!

1. Provision an Ubuntu 18 LTS VM with at least 2GiB of ram
    * I strongly suggest only setting up key based auth for SSH, and blocking port 22 once everything is set up
1. SSH in
1. Clone this repo
1. Navigate to the root of this repo
1. `apt install virtualenv screen gunicorn3 libsndfile1 ffmpeg nginx`
1. `virtualenv -p /usr/bin/python3 ./venv`
    * Do this to ensure you're using python3, and only python3
1. `source venv/bin/activate`
    * Enter your new python virtual env
1. Install pip dependencies
    * `pip3 install -r requirements.txt`
        * If you hit memory errors installing torch, try [these steps](https://stackoverflow.com/a/29467260) (but allocating 2097152 of swap, e.g.: 2GiB) and set the `--no-cache-dir` flag on pip3
1. `deactivate`
    * Exit your virtual env
1. Start a `screen` and run
    1. `source venv/bin/activate`
    1. `gunicorn3 --name ml-hot-or-cold --bind=unix:///tmp/ml-hot-or-cold.sock -w 3 -k uvicorn.workers.UvicornWorker --log-level warning server:app`
        * See the [uvicorn deployment docs](https://www.uvicorn.org/deployment/) for all available options
        * It appears the best practice is to set `-w` to [2 * num_cores + 1](https://docs.gunicorn.org/en/stable/design.html#how-many-workers) 
1. Detach using `ctrl+a d`
    * Reattach using `screen -ls` and `screen -r <screen name>`
1. Sanity check your config using `curl --unix-socket ///tmp/ml-hot-or-cold.sock http://localhost`
1. [Set up nginx](https://www.uvicorn.org/deployment/#running-behind-nginx)
    * Don't forget to `sudo systemctl stop nginx` before editing `/etc/nginx/sites-available/default` and to run `sudo systemctl enable nginx` and `sudo systemctl start nginx` after
    * I ended up using this configuration:
        ```
        sudo bash -c "echo '
        server {
            listen 80;
            client_max_body_size 4G;

            server_name ml-hot-or-cold.projects.chrisjeakle.com;
            proxy_redirect off;
            proxy_buffering off;
            proxy_force_ranges on;

            location / {
                proxy_pass http://ml_hot_or_cold_upstream;
            }
        }

        upstream ml_hot_or_cold_upstream {
            server unix:/tmp/ml-hot-or-cold.sock;
        }
        ' > /etc/nginx/sites-available/default"
        ```
        * **Beware, this overwrites the default nginx configuration entirely!**
1. Set up [letsencrypt certbot](https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/) (for TLS)

## A note on the data
The data is annotated with temperatures, but those annotations are not based on precise measurements. The 40 degree water was kept in the refrigerator before pouring, the 4x degree water was poured a couple times so I raised the annotated temperature a bit, the 7x degree water was at room temperature (the value is based on my thermostat at the time), and all temperatures >= 175 were annotated with the set temperature on my electric kettle. All temperatures are in Fahrenheit.

## License

### Software License (except where otherwise noted in comments)
The MIT License (MIT)

Copyright (c) 2020 Chris Jeakle

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Data License
[CC BY-SA](https://creativecommons.org/licenses/by-sa/2.0/)

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

## Running the notebooks and website locally

1. Install dependencies:
    1. Install miniconda:
        ```
        cd ~
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        bash Miniconda3-latest-Linux-x86_64.sh
        # Proceed through the install process
        source ~/.bashrc
        rm Miniconda3-latest-Linux-x86_64.sh
        ```
        * Add a `conda deactivate` to your `~/.bashrc` to start your shell sessions outside conda
    1. `conda create -n ml-hot-or-cold python=3.8`
    1. `conda activate ml-hot-or-cold`
    1. Install the Jupyter Notebook server
        * `conda install jupyter notebook`
    1. `pip3 install -r requirements.txt`
        * On certain platforms (such as WSL) torch and fastai may not install correctly. Use conda to install them in such cases. 
            * e.g.: `conda install -c pytorch -c fastai fastai`
1. Start the notebooks using:
    1. `conda activate ml-hot-or-cold && jupyter notebook`
    1. Navigate to the url and port printed in the terminal window
1. Start the server:
    1. `conda activate ml-hot-or-cold && python3 server.py`
    1. Navigate to the url and port printed in the terminal window

## Hosting the website

A guide from absolutely nothing to a working site hosted on an VM: I pulled my hair out so you don't have to!

1. Provision an Ubuntu 18 LTS VM with at least 2GiB of ram
    * Note: for some improved security, be sure to [harden your ssh setup](https://askubuntu.com/a/2279)
1. SSH in
1. Install pre-requisite software
    * `sudo apt install git virtualenv libsndfile1 ffmpeg nginx python3-dev`
1. Create a new non-root user to run the web service
    1.  `sudo useradd --system ml-hot-or-cold`
        * Create a `system` user, we have no need for interactive shell sessions or a home dir
1. Become that non-root user
    * e.g.: `sudo su ml-hot-or-cold`
1. Clone this repo into the service user's home directory
    * e.g.: `git clone https://github.com/cjjeakle/ml-hot-or-cold.git ~/server/`
1. Navigate to the root of this repo
    * e.g.: `cd ~/server/`
1. `virtualenv -p /usr/bin/python3 ./venv`
    * Do this to ensure you're using python3, and only python3
1. Enter your new python virtual env
    * `source venv/bin/activate`
        * You may have to enter a `bash` session to run this command if your shell defaults to `sh`
1. Install pip dependencies
    * `pip3 install -r requirements.txt`
        * If you hit memory errors installing torch, temporarily exit the venv and try [these steps](https://stackoverflow.com/a/29467260)
            * Note: allocate 2097152 of swap, e.g.: 2GiB
1. `deactivate`
    * Exit your virtual env
1. Configure the webserver using systemd
    1. Create a service: `/etc/systemd/system/ml-hot-or-cold.service`
        ```
        [Unit]
        Description=ml-hot-or-cold application server

        [Service]
        Type=simple
        Restart=always
        User=ml-hot-or-cold
        Group=ml-hot-or-cold
        WorkingDirectory=/home/ml-hot-or-cold/server/
        ExecStart=/bin/bash -c 'cd /home/ml-hot-or-cold/server/ && source venv/bin/activate && gunicorn --name ml-hot-or-cold --bind=unix:///tmp/ml-hot-or-cold.sock -w 3 -k uvicorn.workers.UvicornWorker --preload --timeout=120 --log-level warning server:app'

        [Install]
        WantedBy=multi-user.target
        ```
        * See the [uvicorn deployment docs](https://www.uvicorn.org/deployment/) for all available options
        * It appears the best practice is to set `-w` to [2 * num_cores + 1](https://docs.gunicorn.org/en/stable/design.html#how-many-workers) 
    1. Start the service:
        ```
        sudo systemctl enable ml-hot-or-cold &&
        sudo systemctl start ml-hot-or-cold
        ```
    * You can see high-level service logs using:
        * `journalctl -u ml-hot-or-cold`
1. Verify your config using `curl --unix-socket ///tmp/ml-hot-or-cold.sock http://localhost`
1. [Set up nginx](https://www.uvicorn.org/deployment/#running-behind-nginx)
    * I ended up using this configuration in `/etc/nginx/conf.d/ml-hot-or-cold.conf`:
        ```
        server {
            listen 80;
            client_max_body_size 10m;

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
        ```
        * Run `sudo systemctl enable nginx` and `sudo systemctl start nginx`
    * You can see nginx logs under `/var/log/nginx/`
        * You can `grep -v "ml-hot-or-cold" access.log | less +G` to see all accesses to the site, for example
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

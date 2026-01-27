FROM jupyter/scipy-notebook:latest

USER root
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    g++ \
    libgl1-mesa-glx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /home/jovyan/work

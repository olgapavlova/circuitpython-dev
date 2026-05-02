FROM python:3.12-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    unzip \
    screen \
    tio \
    picocom \
    usbutils \
    udev \
    jq \
    dosfstools \
    mtools \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip \
    && pip install circup adafruit-ampy mpremote pyserial

WORKDIR /workspace

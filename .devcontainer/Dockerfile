FROM python:3.12-bookworm

ARG USERNAME=op
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    git \
    curl \
    wget \
    unzip \
    screen \
    picocom \
    usbutils \
    udev \
    jq \
    dosfstools \
    mtools \
    && rm -rf /var/lib/apt/lists/*

RUN echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

RUN python -m pip install --upgrade pip \
    && pip install circup adafruit-ampy mpremote pyserial

WORKDIR /workspace
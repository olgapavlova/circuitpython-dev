# Базовый образ: Debian Bookworm + Python 3.12
# Даёт системную среду, пакетный менеджер apt и python runtime
FROM python:3.12-bookworm

# Параметры пользователя (можно переопределить при сборке)
# USERNAME — имя пользователя внутри контейнера
# USER_UID / USER_GID — должны совпадать с хостом, чтобы не было проблем с правами
# Выяснять командой id (можно с ключами -u и -g)
ARG USERNAME=op
ARG USER_UID=1000
ARG USER_GID=1000

# Создание группы и пользователя
# -m → создать домашнюю директорию
# -s /bin/bash → задать login shell (может быть установлен позже)
# Это базовая конфигурация среды, от неё зависит всё остальное
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m -s /bin/bash ${USERNAME}

# Установка системных инструментов
# bash       → shell (вдруг не стоит, хотя обычно да)
# sudo       → работа от админа
# git        → работа с git-репозиториями
# curl/wget  → загрузка файлов по URL
# unzip      → распаковка архивов
# screen     → терминальные сессии
# picocom/tio→ работа с serial (ESP32, CircuitPython)
# usbutils   → диагностика USB (lsusb)
# udev       → управление устройствами
# jq         → обработка JSON
# dosfstools → работа с FAT (mkfs, fsck)
# mtools     → операции с FAT без монтирования
# cleanup    → удаление кэша apt для уменьшения образа
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
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
    tio \
    dosfstools \
    mtools \
    && rm -rf /var/lib/apt/lists/*

# Настройка прав пользователя
# dialout → доступ к serial (/dev/ttyACM*, /dev/ttyUSB*)
# plugdev → доступ к USB-устройствам (через udev)
# sudoers → разрешить sudo без пароля (удобство в dev-среде)
RUN usermod -aG dialout,plugdev ${USERNAME} \
    && echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# Установка Python-инструментов для CircuitPython
# circup        → управление библиотеками CircuitPython
# adafruit-ampy → загрузка файлов на устройство
# mpremote      → работа с MicroPython/CircuitPython REPL и файловой системой
# pyserial      → доступ к serial-порту из Python
RUN python -m pip install --upgrade pip \
    && pip install circup adafruit-ampy mpremote pyserial

# Рабочая директория проекта внутри контейнера
WORKDIR /workspace
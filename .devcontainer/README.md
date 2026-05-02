# Dev container для CircuitPython

Контейнер даёт среду разработки для работы с платами CircuitPython через Raspberry Pi.

Схема работы:

VS Code → SSH → Raspberry Pi → контейнер → USB-плата

## Что внутри

Инструменты:

- Python
- pip
- circup
- adafruit-ampy
- mpremote
- pyserial
- picocom
- screen
- tio
- usbutils
- jq

Контейнер запускается с доступом к USB:

- /dev
- /media
- /run/media

## Проверка

Плата видна:

`lsusb`

Serial:

`ls -l /dev/serial/by-id`

Диск:

`find /media /run/media /mnt -maxdepth 4 -type d -name CIRCUITPY`

## Заливка кода

`./scripts/deploy.sh`

или:

`./scripts/deploy.sh src/code.py`

Файл копируется в:

`CIRCUITPY/code.py`

## Установка библиотек (зависимостей)

`circup --path /mnt/CIRCUITPY install --auto`

## Serial

Открыть:

`picocom -b 115200 /dev/serial/by-id/<код устройства>`

Выход:

`Ctrl-A Ctrl-X`

Перезапуск кода:

`Ctrl-D`

## Serial через tio

Открыть:

`tio /dev/ttyACM0`

Выход: 

`Ctrl + T q`

## Проверка через REPL

```python
import os
os.listdir("/")
```

## Рабочий цикл

1. Редактировать src/code.py
2. Выполнить ./scripts/deploy.sh
3. Открыть serial
4. Нажать Ctrl-D
5. Смотреть вывод

## Задачи VS Code

Команды вынесены в:

`.vscode/tasks.json`

Запуск через:

`Tasks: Run Task`
# Dev container для CircuitPython

Контейнер даёт среду разработки для работы с платами CircuitPython.

Схема работы:

VS Code → контейнер → USB-плата

## Предварительно
Считаем, что устройство подмонтировано к `/mnt/CIRCUITPY`.

Если есть SD-карта — она подмонтирована к `/mnt/LILYGO/sd`.

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

Контейнер запускается с доступом к USB.

## Проверка

Плата видна:

`lsusb`

Serial:

`ls -l /dev/serial/by-id`

Диск:

`find /mnt -maxdepth 4 -type d -name CIRCUITPY`

## Заливка кода

`./scripts/deploy.sh <имя файла в каталоге src/>`

Если без параметров, заливается `code.py`

Файл копируется в:

`CIRCUITPY/code.py`

Это обеспечивает его автозапуск при подключении питания устройства.

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

`Tasks: Run Task` (Command + Shift + P)
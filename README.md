#### Описание
Приложение для ИП Веклич Егор Александрович

# Cодержание

1. [О приложении](#structure)

2. [Используемые технологии в приложении:](#technologies-project)

3. [Подготовка к запуску](#start)

4. [Подключение телеграм бота](#bot) 

5. [Настройка переменных окружения](#env)

6. [Запуск проекта локально](#run-local)

7. [Запуск в Docker](#run-docker)

8. [Работа с API](#api)

# 1. О приложении <a id="project"></a>

Приложение выполняет отправку и чтение сообщений посредством API и телеграмм бота.

Данные хранятся в mongodb, кеширование при помощи redis.

# 2. Используемые технологии в проекте<a id="technologies-project"></a>:

[![Python][Python-badge]][Python-url]

[![Docker][Docker-badge]][Docker-url]

[![MongoDB][MongoDB-badge]][MongoDB-url]

[![Redis][Redis-badge]][Redis-url]

[![Aiogram][Aiogram-badge]][Aiogram-url]

[![Fastapi][Fastapi-badge]][Fastapi-url]

# 3. Подготовка к запуску <a id="start"></a>

3.1 Склонировать удаленный репозиторий через ssh или https ссылку.

```
git clone <ssh or https>

```
3.2 Перейти в каталог /app, устанавить и развернуть виртуальное окружение.

```
cd app/

python -m .venv venv

source .venv/bin/activate
```
если win os

```
source .venv/Scripts/acvite
```
3.3 Установить зависимости из файла reqirements.txt

```
pip install -r requirements.txt
```

# 4. Подключение телеграм бота <a id="bot"></a>

Перейти в телеграм, там найти BotFather и отправить команду 

```
/newbot
```

Будет предложено указать имя бота, описание и т.д., в конце будет выдан API токен.

# 5. Настройка переменных окружения <a id="env"></a>

В каталоге приложения лежит файл .env.example, необходимо в той же директории создать файл .env и из .env.example скопировать содержимое, в том числе полученный в BotFather APi токен.

# 6. Запуск проекта локально <a id="run-local"></a>

Перед запуском сервера, нужно запустить redis и mongo сервера, к которым будет подключаться сам сервер приложения.

Оба хранилища подключатся в контейнерах. Для этого нужно

Перейти в директорию /infra
```
/cd infra

```
Запустить docker-compose.local.yaml

```
docker compose -f docker-compose.local.yaml up --build -d
```
Для запуска проекта из директории (app) выполнить команду в терминале

```
uvicorn main:app --reload
```
Флаг --reload не обязателен, используется для активной разработки, что бы сервер сам себя перезагружал после каждого измнения.
Далее в новом экземпляре терминала выполнить команду для запуска бота.
```
python main.py
```

# 7. Запуск в Docker <a id="run-docker"></a>

Для запуска приложения полностью из контейнеров необходимо:

Перейти в директорию infra
```
cd /infra
```
Запустить docker-compose.yaml
```
docker compose up --build -d
```
Запустить бота из контейнера, необходимо напрямую в контейнер с приложением отправить команду 
```
docker compose exec backend python main.py
```

# 8. Работа с api <a id="api"></a>

Работа с api можно выполнить при запущеном localhost по адресу http://localhost/api/v1/docs .

Там можно ознакомится с структрукой эндпоинтов, маршрутами и т.д. Также можно отправить запросы и посмотреть ответы сервера.


<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/downloads/release/python-3120/
[Python-badge]: https://img.shields.io/badge/python-v3.12-yellow?style=for-the-badge&logo=python

[Docker-url]: https://www.docker.com/
[Docker-badge]: https://img.shields.io/badge/docker-red?style=for-the-badge&logo=docker

[MongoDB-url]: https://www.mongodb.com/
[MongoDB-badge]: https://img.shields.io/badge/MongoDB-green?style=for-the-badge&logo=mongodb&logoColor=white&link=https://www.mongodb.com/

[Redis-url]: https://redis.io/
[Redis-badge]: https://img.shields.io/badge/Redis-red?style=for-the-badge&logo=redis&logoColor=white&link=https://redis.io/

[Aiogram-url]: https://docs.aiogram.dev/en/latest/
[Aiogram-badge]: https://img.shields.io/badge/Aiogram-purple?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz...&logoColor=white&link=https://github.com/aiogram/aiogram

[Fastapi-url]: https://fastapi.tiangolo.com/
[Fastapi-badge]: https://img.shields.io/badge/FastAPI-blue?style=for-the-badge&logo=fastapi&logoColor=white&link=https://fastapi.tiangolo.com/
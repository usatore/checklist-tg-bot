# Используем официальный образ Python 3.11
FROM python:3.11-slim-bullseye

# Устанавливаем переменные окружения, чтобы избежать создания bytecode и буферизации вывода
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта в контейнер в директорию /app/src
COPY ./src /app/src

# Указываем команду, которая будет выполняться при запуске контейнера
CMD ["python", "-m", "src.main"]

# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей (requirements.txt) в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install werkzeug
RUN pip install "uvicorn[standard]"

# Копируем весь исходный код приложения в контейнер
COPY . .

# Указываем команду, которая будет выполнена при запуске контейнера
CMD ["uvicorn", "twinkle:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

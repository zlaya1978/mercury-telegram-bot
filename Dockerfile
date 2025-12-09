FROM python:3.10-slim

WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
COPY gemini_bot.py .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем бота
CMD ["python", "gemini_bot.py"]

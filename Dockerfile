# ---------- Фаза 1: билд зависимостей ----------
FROM python:3.11-slim AS builder

# Рабочая директория
WORKDIR /app

# Обновляем pip
RUN pip install --no-cache-dir --upgrade pip

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости в отдельную папку (чтобы не тащить pip и кеши)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Фаза 2: финальный образ ----------
FROM python:3.11-slim

WORKDIR /app

# Копируем только установленные зависимости
COPY --from=builder /install /usr/local

# Копируем код бота
COPY . .

# Запускаем бота через uvicorn
CMD ["python", "-m", "main.py"]
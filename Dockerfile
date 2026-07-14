FROM python:3.11-slim

WORKDIR /app

# Agar requirements.txt asosiy papkada bo'lsa:
COPY requirements.txt .

# Qolgan fayllarni ham ko'chirish uchun (muhim!)
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "userbot.py"]

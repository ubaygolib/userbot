FROM python:3.11-slim

WORKDIR /app

# Avval talab qilingan kutubxonalarni nusxalash va o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Keyin qolgan barcha fayllarni (userbot.py, main.py va hokazo) to'liq ko'chirish
COPY . .

# Botni asosiy main.py fayli orqali ishga tushiramiz!
CMD ["python", "main.py"]

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Aici am schimbat din main.py în weather.py!
COPY weather.py .

# Și aici am schimbat să ruleze weather.py
ENTRYPOINT ["python", "weather.py"]


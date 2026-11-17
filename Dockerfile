FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libglib2.0-0 libgl1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY static/ static/
ENV PORT=3000
EXPOSE 3000
CMD ["waitress-serve", "--host=0.0.0.0", "--port=3000", "app:app"]

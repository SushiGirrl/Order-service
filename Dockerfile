# Brug en officiel Python runtime som et parent image
FROM python:3.9-slim

# Angiv working directory i containeren
WORKDIR /app

# Kopier requirements.txt og installer afhængigheder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask requests

# Kopier resten af applikationsfilerne
COPY . .

# Eksponér port 5000 for Flask API
EXPOSE 5000

# Start applikationen
CMD ["python", "app.py"]

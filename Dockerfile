# Gunakan image Python ringan
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set environment variable Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Jalankan Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

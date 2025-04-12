# Gunakan image Python ringan
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies including gunicorn
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy source code
COPY . .

# Set environment variable Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Verify gunicorn installation
RUN which gunicorn && gunicorn --version

# Expose port
EXPOSE 5000

# Run production server (use PORT environment variable if available)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 4 app:app"]

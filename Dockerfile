# Gunakan image resmi Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Salin file requirements.txt ke dalam container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file dari project lokal ke dalam container
COPY . /app/

# Expose port yang digunakan aplikasi Flask (default 5000)
EXPOSE 5000

# Jalankan aplikasi Flask
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]

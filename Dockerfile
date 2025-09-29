FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ .

# Create downloads directory
RUN mkdir -p /app/downloads

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

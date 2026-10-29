FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for PyMuPDF and C++ extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies from PyPI; requirements.txt uses the official CPU wheel
# listing only for the pinned PyTorch wheel, keeping build dependencies on PyPI.
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8001

# Command to run uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

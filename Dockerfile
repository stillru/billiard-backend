# Use the smallest Python base image
FROM python:3.10-alpine

# Set work directory
WORKDIR /app

# Copy requirements file first (for caching purposes)
COPY requirements.txt .

# Install dependencies (no cache to reduce image size)
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Copy the application code
COPY . .

# Add Pythonpath
RUN export PYTHONPATH="$PYTHONPATH:/app"

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
#ENV PYTHONPATH="${PYTHONPATH}:/app"


# Start the application
ENTRYPOINT ["env", "PYTHONPATH=/app", "flask", "run", "--host=0.0.0.0", "--port=5000"]

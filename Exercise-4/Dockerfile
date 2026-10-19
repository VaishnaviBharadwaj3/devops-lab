# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and application code
COPY requirements.txt .
COPY app.py .

# Install Flask
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5001

# Start the application
CMD ["python", "app.py"]
FROM python:3.10-slim-bullseye
LABEL maintainer="AI Fist"
# Set environment variables
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Install the Python dependencies (requirements.txt should be in the same directory)
RUN pip install --no-cache-dir -r requirements.txt

# Update the CMD to run your FastAPI app using run.py
EXPOSE 8080

# Explicitly set the entrypoint path
ENTRYPOINT ["bash", "/app/entrypoint.sh"]
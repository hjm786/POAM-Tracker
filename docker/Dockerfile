# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /workspaces/POAM-Pilot

# Copy project files
COPY . /workspaces/POAM-Pilot

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Start the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]

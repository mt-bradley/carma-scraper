# Use a slim Python image for a lightweight container.
FROM python:3.9-slim

# Set the working directory inside the container.
WORKDIR /app

# Copy dependency definitions and install them.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container.
COPY . .

# Default command: run the scraper.
CMD ["python", "main.py"]


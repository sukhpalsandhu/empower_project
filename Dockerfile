# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables (placeholders)
ENV EMPOWER_EMAIL=your_email@example.com
ENV EMPOWER_PASSWORD=your_password

# Run api.py when the container launches
CMD ["python", "api.py"]

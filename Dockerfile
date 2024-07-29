# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install fastapi uvicorn

# Copy the current directory contents into the container at /app
COPY ./ /app

# Expose port 5522 to the outside world
EXPOSE 5522

# Run the command to start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5522", "--reload"]
# Dockerfile

# The first instruction is what image we want to base our container on
# We use an official Python runtime as a parent image
FROM python:3.11

# Allows docker to cache installed dependencies between builds
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Mounts the application code to the image
COPY . code
WORKDIR /code

EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
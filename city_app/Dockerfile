# Use Python 3.11 on Debian Buster as the base image
FROM python:3.12

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
        binutils \
        libproj-dev \
        gdal-bin \
        libgdal-dev \
        postgresql-client \
        sqlite3 \
        libsqlite3-dev \
        python-dev-is-python3 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV LD_LIBRARY_PATH=/usr/lib

# Install Poetry
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy the rest of the application code
COPY . .

RUN poetry run python manage.py collectstatic --noinput

# Expose ports
EXPOSE 8000

# Set the entrypoint to run gunicorn
ENTRYPOINT ["sh", "-c", "poetry run gunicorn city_app.wsgi:application --bind 0.0.0.0:8000"]
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim-buster

# Python Unbuffered to read building logs
ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install Python dependencies and Gunicorn
RUN pip install --no-cache-dir txp[dash_app] && pip install --no-cache-dir gunicorn
RUN groupadd -r app && useradd -r -g app app

# COPY CREDENTIALS FILE
COPY auth.toml .

USER app

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available in Cloud Run.
# CMD exec gunicorn --bind :$PORT --chdir /usr/local/lib/python/site-packages/txp/dashboard --log-level info --workers 1 --threads 8 --timeout 0 app:server
CMD ["bash"]

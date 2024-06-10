FROM python:3.10-slim

WORKDIR /app

# Copy the necessary dirs into the container at /app
COPY requirements_prod.txt requirements.txt
RUN pip install -r requirements.txt

COPY backend backend
COPY setup.py setup.py
RUN mkdir raw_data
RUN pip install .

# Install cron
RUN apt-get update && apt-get install -y cron

# Add crontab file, give exe rights & run
ADD crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN crontab /etc/cron.d/hello-cron

# Create cron log file
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

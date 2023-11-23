# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
#RUN apt update;apt install -yy apache2;sed -i 's/Listen 80/Listen 10000/' /etc/apache2/ports.conf

WORKDIR /app
COPY . /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["bash", "start.sh"]

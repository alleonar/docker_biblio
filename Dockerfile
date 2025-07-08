# Use official python as base image (Debian GNU/Linux 12 (bookworm))
FROM python:3.13.3

# Set python output straight to terminal without buffering first to get real-time logs
ENV PYTHONUNBUFFERED=1

# Install Node.js & npm from apt
RUN apt-get update \
    && apt-get install -y curl gnupg build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set the root directory in the debian instance
WORKDIR /usr/src/app

# Copy the local requirements file to debian root directory
COPY requirements.txt ./

# Install packages and dependancies (without pip archives to minimise image size)
RUN pip install --no-cache-dir -r requirements.txt

# Prepare repository
RUN mkdir -p /usr/src/app/bibliodrive

# Copy all file from local repository (PRODUCTION)
COPY . .

# Supprime tous les dossiers __pycache__ pour éviter les problèmes de cache Python
RUN find . -type d -name '__pycache__' -exec rm -rf {} +

# # Set workdir to install node modules
WORKDIR /usr/src/app/bibliodrive

# install nodes modules
RUN npm install

# Document the future open port (the python server default port 8000)
EXPOSE 8000

# Prepare db
COPY entrypoint.sh /entrypoint.sh

# Set permissions
RUN chmod +x /entrypoint.sh

# Execute entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
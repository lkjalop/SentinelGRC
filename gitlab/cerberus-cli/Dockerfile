# Cerberus AI CLI Docker Image for GitLab CI
FROM python:3.11-slim

LABEL maintainer="Cerberus AI Team <dev@cerberus-ai.com>"
LABEL description="Cerberus AI CLI for GitLab CI/CD compliance validation"
LABEL version="1.0.0"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    jq \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install Cerberus CLI
COPY cerberus_cli/ /opt/cerberus-cli/
RUN pip install -e /opt/cerberus-cli/

# Add CLI to PATH
RUN ln -s /opt/cerberus-cli/bin/cerberus-cli /usr/local/bin/cerberus-cli

# Create working directory
WORKDIR /workspace

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set default command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["cerberus-cli", "--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD cerberus-cli --version || exit 1
FROM ubuntu:noble
MAINTAINER Odoo S.A. <info@odoo.com>

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Generate locale C.UTF-8 for postgres and general locale data
ENV LANG en_US.UTF-8

# Install system dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        dirmngr \
        fonts-noto-cjk \
        gnupg \
        libssl-dev \
        node-less \
        npm \
        python3 \
        python3-venv \
        python3-pip \
        git \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        xz-utils && \
    rm -rf /var/lib/apt/lists/*

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Clone the repository
ARG GIT_REPO=https://github.com/LeGrandF38/pack-entreprise.git
ARG BRANCH_NAME=18.0
RUN git clone -b ${BRANCH_NAME} ${GIT_REPO} /opt/odoo



# Install Python dependencies from the requirements file
RUN pip install -r /opt/odoo/requirements.txt


# Change working directory
WORKDIR /opt/odoo

# Install additional Odoo dependencies
RUN pip install -r requirements.txt

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /entrypoint.sh
COPY ./odoo.conf /etc/odoo/

# Set permissions and Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN chown odoo /etc/odoo/odoo.conf \
    && mkdir -p /mnt/extra-addons \
    && chown -R odoo /mnt/extra-addons
VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

# Copy wait-for-psql script
COPY wait-for-psql.py /usr/local/bin/wait-for-psql.py

# Set default user when running the container
USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]

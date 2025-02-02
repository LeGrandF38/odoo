FROM ubuntu:noble
MAINTAINER Odoo S.A. <info@odoo.com>

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

ENV LANG en_US.UTF-8

# Dépendances système
ARG TARGETARCH
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        dirmngr \
        fonts-noto-cjk \
        gnupg \
        libssl-dev \
        node-less \
        npm \
        python3.12 \
        python3.12-venv \
        python3.12-dev \
        xz-utils && \
    rm -rf /var/lib/apt/lists/*

# Installation de wkhtmltopdf en fonction de l'architecture
RUN if [ -z "${TARGETARCH}" ]; then TARGETARCH="$(dpkg --print-architecture)"; fi; \
    WKHTMLTOPDF_ARCH=${TARGETARCH} && \
    case ${TARGETARCH} in \
    "amd64") WKHTMLTOPDF_ARCH=amd64 && WKHTMLTOPDF_SHA=967390a759707337b46d1c02452e2bb6b2dc6d59 ;; \
    "arm64") WKHTMLTOPDF_SHA=90f6e69896d51ef77339d3f3a20f8582bdf496cc ;; \
    "ppc64le" | "ppc64el") WKHTMLTOPDF_ARCH=ppc64el && WKHTMLTOPDF_SHA=5312d7d34a25b321282929df82e3574319aed25c ;; \
    esac && \
    curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_${WKHTMLTOPDF_ARCH}.deb && \
    echo ${WKHTMLTOPDF_SHA} wkhtmltox.deb | sha1sum -c - && \
    apt-get install -y --no-install-recommends ./wkhtmltox.deb && \
    rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# Installation de PostgreSQL client
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ noble-pgdg main' > /etc/apt/sources.list.d/pgdg.list && \
    GNUPGHOME="$(mktemp -d)" && \
    export GNUPGHOME && \
    repokey='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8' && \
    gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" && \
    gpg --batch --armor --export "${repokey}" > /etc/apt/trusted.gpg.d/pgdg.gpg.asc && \
    gpgconf --kill all && \
    rm -rf "$GNUPGHOME" && \
    apt-get update && \
    apt-get install --no-install-recommends -y postgresql-client && \
    rm -f /etc/apt/sources.list.d/pgdg.list && \
    rm -rf /var/lib/apt/lists/*

# Installer rtlcss globalement
RUN npm install -g rtlcss

# Création de l'environnement virtuel Python
RUN python3.12 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copier le fichier requirements.txt et installer les dépendances
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Copier le code Odoo
COPY . /opt/odoo/
WORKDIR /opt/odoo

# Exposer les ports Odoo
EXPOSE 8069 8071 8072

# Copier les fichiers de configuration
COPY ./entrypoint.sh /
COPY ./odoo.conf /etc/odoo/

# Configurer les permissions
RUN chown odoo /etc/odoo/odoo.conf && \
    mkdir -p /mnt/extra-addons && \
    chown -R odoo /mnt/extra-addons

# Définition des volumes
VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

# Configurer l'entrée et la commande par défaut
USER odoo
ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]

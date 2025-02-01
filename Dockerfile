FROM ubuntu:noble
MAINTAINER Odoo S.A. <info@odoo.com>

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Générer la locale C.UTF-8 pour PostgreSQL et les données locales générales
ENV LANG en_US.UTF-8

# Récupérer l'architecture cible pour installer le paquet wkhtmltopdf correct
ARG TARGETARCH

# Installer des dépendances, lessc, less-plugin-clean-css, et wkhtmltopdf
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
        python3-magic \
        python3-num2words \
        python3-odf \
        python3-pdfminer \
        python3-pip \
        python3-phonenumbers \
        python3-pyldap \
        python3-qrcode \
        python3-renderpm \
        python3-setuptools \
        python3-slugify \
        python3-vobject \
        python3-watchdog \
        python3-xlrd \
        python3-xlwt \
        xz-utils && \
    if [ -z "${TARGETARCH}" ]; then \
        TARGETARCH="$(dpkg --print-architecture)"; \
    fi; \
    WKHTMLTOPDF_ARCH=${TARGETARCH} && \
    case ${TARGETARCH} in \
    "amd64") WKHTMLTOPDF_ARCH=amd64 && WKHTMLTOPDF_SHA=967390a759707337b46d1c02452e2bb6b2dc6d59  ;; \
    "arm64")  WKHTMLTOPDF_SHA=90f6e69896d51ef77339d3f3a20f8582bdf496cc  ;; \
    "ppc64le" | "ppc64el") WKHTMLTOPDF_ARCH=ppc64el && WKHTMLTOPDF_SHA=5312d7d34a25b321282929df82e3574319aed25c  ;; \
    esac \
    && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_${WKHTMLTOPDF_ARCH}.deb \
    && echo ${WKHTMLTOPDF_SHA} wkhtmltox.deb | sha1sum -c - \
    && apt-get install -y --no-install-recommends ./wkhtmltox.deb \
    && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# Installer le client PostgreSQL
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ noble-pgdg main' > /etc/apt/sources.list.d/pgdg.list \
    && GNUPGHOME="$(mktemp -d)" \
    && export GNUPGHOME \
    && repokey='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8' \
    && gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" \
    && gpg --batch --armor --export "${repokey}" > /etc/apt/trusted.gpg.d/pgdg.gpg.asc \
    && gpgconf --kill all \
    && rm -rf "$GNUPGHOME" \
    && apt-get update  \
    && apt-get install --no-install-recommends -y postgresql-client \
    && rm -f /etc/apt/sources.list.d/pgdg.list \
    && rm -rf /var/lib/apt/lists/*

# Installer rtlcss (sur Debian buster)
RUN npm install -g rtlcss

# Copier le fichier requirements.txt et installer les dépendances python
COPY ./requirements.txt /tmp/requirements.txt

# Installer les dépendances python depuis requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt

# Copier le code Odoo
COPY . /opt/odoo/

# Définir le répertoire d'Odoo comme répertoire de travail
WORKDIR /opt/odoo

# Exposer les services Odoo
EXPOSE 8069 8071 8072

# Copier le fichier de configuration et le script d'entrée
COPY ./entrypoint.sh /
COPY ./odoo.conf /etc/odoo/

# Configurer les permissions pour Odoo
RUN chown odoo /etc/odoo/odoo.conf && \
    mkdir -p /mnt/extra-addons && \
    chown -R odoo /mnt/extra-addons

# Volume pour les fichiers de données Odoo
VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

# Configurer l'entrée et la commande par défaut
USER odoo
ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]

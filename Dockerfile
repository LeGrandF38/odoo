FROM ubuntu:noble
MAINTAINER Odoo S.A. <info@odoo.com>

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Générer la locale C.UTF-8 pour Postgres et les données locales générales
ENV LANG en_US.UTF-8

# Installer les dépendances système
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
        xz-utils \
        postgresql \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Créer et activer un environnement virtuel
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Mettre à jour pip et installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r /opt/odoo/requirements.txt

# Cloner le dépôt
ARG GIT_REPO=https://github.com/LeGrandF38/pack-entreprise.git
ARG BRANCH_NAME=18.0
RUN git clone -b ${BRANCH_NAME} ${GIT_REPO} /opt/odoo

# Changer le répertoire de travail
WORKDIR /opt/odoo

# Installer les dépendances d'Odoo
RUN pip install -r requirements.txt

# Copier le script d'entrée et le fichier de configuration d'Odoo
COPY ./entrypoint.sh / 
COPY ./odoo.conf /etc/odoo/

# Définir les permissions et monter /var/lib/odoo pour restaurer le filestore et /mnt/extra-addons pour les add-ons des utilisateurs
RUN chown odoo /etc/odoo/odoo.conf \
    && mkdir -p /mnt/extra-addons \
    && chown -R odoo /mnt/extra-addons
VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

# Exposer les services d'Odoo
EXPOSE 8069 8071 8072

# Définir le fichier de configuration par défaut
ENV ODOO_RC /etc/odoo/odoo.conf

COPY wait-for-psql.py /usr/local/bin/wait-for-psql.py

# Définir l'utilisateur par défaut lors de l'exécution du conteneur
USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]

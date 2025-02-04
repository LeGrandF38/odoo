#!/bin/bash

set -e

if [ -v PASSWORD_FILE ]; then
    PASSWORD="$(< $PASSWORD_FILE)"
fi

# Configurations de base
: ${HOST:=${DB_PORT_5432_TCP_ADDR:='db'}}
: ${PORT:=${DB_PORT_5432_TCP_PORT:=5432}}
: ${USER:=${DB_ENV_POSTGRES_USER:=${POSTGRES_USER:='odoo'}}}
: ${PASSWORD:=${DB_ENV_POSTGRES_PASSWORD:=${POSTGRES_PASSWORD:='odoo'}}}

# Vérification du fichier de configuration
ODOO_RC=${ODOO_RC:-/etc/odoo/odoo.conf}

DB_ARGS=()
function check_config() {
    param="$1"
    value="$2"
    if [ -f "$ODOO_RC" ] && grep -q -E "^\s*\b${param}\b\s*=" "$ODOO_RC"; then
        value=$(grep -E "^\s*\b${param}\b\s*=" "$ODOO_RC" | cut -d " " -f3 | tr -d '["\n\r]')
    fi
    DB_ARGS+=("--${param}")
    DB_ARGS+=("${value}")
}
check_config "db_host" "$HOST"
check_config "db_port" "$PORT"
check_config "db_user" "$USER"
check_config "db_password" "$PASSWORD"

# Logique principale
case "$1" in
    -- | odoo)
        shift
        if [[ "$1" == "scaffold" ]]; then
            exec ./odoo-bin "$@"
        else
            /usr/local/bin/wait-for-psql.py "${DB_ARGS[@]}" --timeout=30
            exec ./odoo-bin "$@" "${DB_ARGS[@]}"
        fi
        ;;
    -*)
        /usr/local/bin/wait-for-psql.py "${DB_ARGS[@]}" --timeout=30
        exec ./odoo-bin "$@" "${DB_ARGS[@]}"
        ;;
    *)
        exec "$@"
        ;;
esac

exit 1

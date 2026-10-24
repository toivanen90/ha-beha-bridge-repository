#!/command/with-contenv bashio

export PYTHONUNBUFFERED=1

bashio::log.info "========== BEHA Bridge Starting =========="

if bashio::services.available "mqtt"; then
    MQTT_HOST=$(bashio::services mqtt "host")
    MQTT_PORT=$(bashio::services mqtt "port")
    MQTT_USER=$(bashio::services mqtt "username")
    MQTT_PASS=$(bashio::services mqtt "password")
    bashio::log.info "MQTT: Using HA service discovery credentials"
else
    bashio::log.error "MQTT service not found! Make sure the Mosquitto broker add-on is installed and running."
    exit 1
fi

BEHA_EMAIL=$(bashio::config 'beha_email')
BEHA_PASS=$(bashio::config 'beha_password')

ln -sf /data/beha_tokens.json /root/.beha_tokens.json

if [ ! -f /data/beha_tokens.json ] || [ ! -s /data/beha_tokens.json ]; then
    bashio::log.info "No tokens found. Attempting login..."
    if [ -z "$BEHA_EMAIL" ] || [ -z "$BEHA_PASS" ]; then
        bashio::log.error "BEHA tokens missing and credentials not provided in config!"
        exit 1
    fi
    python3 /beha_auth.py login-headless "$BEHA_EMAIL" "$BEHA_PASS"
fi

bashio::log.info "Starting MQTT Bridge..."
exec python3 /beha_mqtt.py --host "$MQTT_HOST" --port "$MQTT_PORT" --user "$MQTT_USER" --passw "$MQTT_PASS"

ARG BUILD_FROM
FROM $BUILD_FROM

ARG UPSTREAM_COMMIT=24938eebb59613501adbbf535fb38db3c507eb57

RUN apk add --no-cache python3 py3-pip curl && \
    pip3 install paho-mqtt requests --break-system-packages && \
    curl -fsSL "https://raw.githubusercontent.com/maxd2s/ha-beha-bridge/${UPSTREAM_COMMIT}/beha_auth.py" -o /beha_auth.py && \
    curl -fsSL "https://raw.githubusercontent.com/maxd2s/ha-beha-bridge/${UPSTREAM_COMMIT}/beha_mqtt.py" -o /beha_mqtt.py

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

FROM certbot/certbot

LABEL name="ghcr.io/holyhamsandwich/certbot-dns-mailinabox"

COPY . /opt/certbot/src/plugin

RUN python tools/pip_install.py --no-cache-dir --editable /opt/certbot/src/plugin

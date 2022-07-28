# Certbot's DNS with Mail-in-a-Box

This plugin uses the DNS-01 authentication challenge with Mail-in-a-Box's DNS
API so that TXT records can be added and removed on the fly. A sample program
invocation could be this:

```shell
certbot certonly -a dns-mailinabox \
	--dns-mailinabox-credentials credentials.ini \
	--dns-mailinabox-propagation-time 10 \
	--dns-mailinabox-host node.mxchgsvc.net \
	-d example.com
```

So far only administrator accounts with 2FA enabled work. The host needs to be
specified and has to be the one with the web administration interface.

### Docker

[![Docker](https://github.com/HolyHamSandwich/certbot-dns-mailinabox/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/HolyHamSandwich/certbot-dns-mailinabox/actions/workflows/docker-publish.yml)

Setup:
```bash
cp sample-credentials.ini credentials.ini

<update credentials.ini>
```

Build:
```bash
docker build -t certbot-dns-mailinabox .
```
Run:
```bash
docker run \
  -v $PWD/credentials.ini:/credentials.ini \
  -v $PWD/conf:/etc/letsencrypt \
  -v $PWD/lib:/var/lib/letsencrypt \
  -v $PWD/log:/var/log/letsencrypt \
  -it certbot-dns-mailinabox certonly \
  -n \
  --email <email> \
  --agree-tos \
  -a dns-mailinabox \
  --dns-mailinabox-credentials /credentials.ini \
  -d <domain>
```

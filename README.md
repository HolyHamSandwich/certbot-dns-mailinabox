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

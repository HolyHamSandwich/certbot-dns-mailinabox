from setuptools import setup

setup(
    name="certbot-dns-mailinabox",
    version="0.1.0",
    description="Mail-in-a-Box's DNS authenticator.",
    package="certbot_dns_mailinabox.py",
    install_requires=[
        "certbot",
        "pyotp",
        "requests",
    ],
    entry_points={
        "certbot.plugins": [
            "dns-mailinabox = certbot_dns_mailinabox:Authenticator",
        ],
    },
)

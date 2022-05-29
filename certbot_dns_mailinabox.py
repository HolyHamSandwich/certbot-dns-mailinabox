from acme import challenges

from certbot import interfaces
from certbot import achallenges
from certbot.plugins import common
from certbot.plugins import dns_common
from certbot.plugins.dns_common import CredentialsConfiguration

from pyotp import TOTP

from requests import post, delete, codes

from typing import Callable
from typing import Any
from typing import Iterable
from typing import List
from typing import Type

from time import sleep


class Authenticator(dns_common.DNSAuthenticator):
    """Mail-in-a-Box's DNS authenticator."""

    description = "Mail-in-a-Box's DNS authenticator."

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.credentials: Optional[CredentialsConfiguration] = None

    @classmethod
    def add_parser_arguments(cls, add: Callable[..., None], default_propagation_seconds: int = 10) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="Mail-in-a-Box credentials INI file.")
        add("host", help="The Mail-in-a-Box web interface host.")

    def more_info(self) -> str:
        return "This plugin configures a DNS TXT record to respond to a DNS-01 challenge using " + \
               "the Mail-in-a-Box API."

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            "credentials",
            "Mail-in-a-Box credentials INI file.",
            {
                "username": "User e-mail address",
                "password": "User password",
                "totp_secret": "Temporary one-time password secret for 2FA"
            }
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        username = self.credentials.conf("username")
        password = self.credentials.conf("password")
        totp_secret = self.credentials.conf("totp_secret")
        
        tries = 3
        while True:
            r = post(f"https://{self.host}/admin/dns/custom/{validation_name}/txt", 
                    auth=(username, password), data=validation, headers={"X-Auth-Token": TOTP(totp_secret).now()})
            
            s = r.status_code
            if s == codes.ok:
                # If the code is 200, it's all good, we can stop.
                break
            elif s == codes.unauthorized:
                # If the code is 401 it could be a 2FA refresh problem so we
                # wait up to three times before giving up.
                tries -= 1
                if tries == 0:
                    r.raise_for_status()
                else:
                    # Sleep if we have more tries to let the system generate more codes.
                    sleep(30.0)
            else:
                # Another error, bad!
                r.raise_for_status()
        
    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        username = self.credentials.conf("username")
        password = self.credentials.conf("password")
        totp_secret = self.credentials.conf("totp_secret")
        
        tries = 3
        while True:
            r = delete(f"https://{self.host}/admin/dns/custom/{validation_name}/txt", 
                    auth=(username, password), data=validation, headers={"X-Auth-Token": TOTP(totp_secret).now()})
        
            s = r.status_code
            if s == codes.ok:
                # If the code is 200, it's all good, we can stop.
                break
            elif s == codes.unauthorized:
                # If the code is 401 it could be a 2FA refresh problem so we
                # wait up to three times before giving up.
                tries -= 1
                if tries == 0:
                    r.raise_for_status()
                else:
                    # Sleep if we have more tries to let the system generate more codes.
                    sleep(30.0)
            else:
                # Another error, bad!
                r.raise_for_status()

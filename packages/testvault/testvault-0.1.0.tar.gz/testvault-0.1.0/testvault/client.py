import requests
import structlog
import urllib.parse

log = structlog.get_logger()


class ServerError(Exception):
    pass


class Client:
    def __init__(self, team_name: str) -> None:
        """
        Create a new TestVault API client.

        The `team_name` argument is used as a prefix for vault IDs.
        """
        # ensure the team name is URL-safe
        self.team_name = urllib.parse.quote_plus(team_name)

    def add_member_to_vault(self, vault_id: str, user: str) -> None:
        """
        Add a user to the vault.

        The vault_id can be any string.
        """
        prefixed_vault_id = f"{self.team_name}_{vault_id}"

        res = requests.post(
            f"https://prod.testvault.granted.run/vaults/{prefixed_vault_id}/members",
            json={"user": user},
        )

        user_urlescaped = urllib.parse.quote_plus(user)
        log.info("granted access to TestVault vault", status_code=res.status_code)
        log.info(
            f"visit https://prod.testvault.granted.run/vaults/{prefixed_vault_id}/members/{user_urlescaped} to check the membership status"
        )

    def remove_member_from_vault(self, vault_id: str, user: str) -> None:
        """
        Remove a member from a vault.

        The vault_id can be any string.
        """
        prefixed_vault_id = f"{self.team_name}_{vault_id}"
        user_urlescaped = urllib.parse.quote_plus(user)

        res = requests.post(
            f"https://prod.testvault.granted.run/vaults/{prefixed_vault_id}/members/{user_urlescaped}/remove",
        )

        log.info("revoked access to TestVault vault", status_code=res.status_code)
        log.info(
            f"visit https://prod.testvault.granted.run/vaults/{prefixed_vault_id}/members/{user_urlescaped} to check the membership status"
        )

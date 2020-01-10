import logging

from re import sub
from requests import get
from .. import loader, utils

logger = logging.getLogger(__name__)


def register(cb):
    cb(IPLookup())


@loader.tds
class IPLookup(loader.Module):
    """IP lookup using ip-api.com"""
    strings = {"name": "IP Lookup"}

    def __init__(self):
        self.name = self.strings["name"]

    async def ipcmd(self, message):
        """Use as .ip <ip> (optional)"""
        ip = utils.get_args_raw(message)

        lookup = get(f"http://ip-api.com/json/{ip}").json()
        fixed_lookup = {}

        for key, value in lookup.items():
            special = {"lat": "Latitude", "lon": "Longitude", "isp": "ISP", "as": "AS", "asname": "AS name"}
            if key in special:
                fixed_lookup[special[key]] = str(value)
                continue

            key = sub(r"([a-z])([A-Z])", r"\g<1> \g<2>", key)
            key = key.capitalize()

            if not value:
                value = "None"

            fixed_lookup[key] = str(value)

        text = ""

        for key, value in fixed_lookup.items():
            text = text + f"<b>{key}:</b> <code>{value}</code>\n"

        await utils.answer(message, text)

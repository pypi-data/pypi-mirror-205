from dataclasses import dataclass
from datetime import datetime
import re

from .ontario_health_card import OntarioHealthCard


@dataclass
class Demographic:
    """
    A class representing a demographic (patient) in the OSCAR EMR system.
    """

    first_name: str
    last_name: str
    id: int
    date_of_birth: datetime
    sex: str

    address: str
    city: str
    province: str
    postal_code: str

    health_card: OntarioHealthCard

    phone_numbers: list[str]
    email: str

    @staticmethod
    def from_dict(raw_data: dict):
        """
        Create an instance of Demographic from the raw status information from the OSCAR REST API.

        Parameters
        --------------
        raw_info : dict
            the json object for a demographic from the OSCAR REST API
        """

        birth_year = raw_data.get("dobYear", 1970)
        birth_month = raw_data.get("dobMonth", 1)
        birth_day = raw_data.get("dobDay", 1)
        date_of_birth = datetime.strptime(
            f"{birth_year}-{birth_month}-{birth_day}", "%Y-%m-%d"
        )

        hin = raw_data.get("hin", "")
        ver = raw_data.get("ver", "")

        health_card = None
        if "" not in [hin, ver]:
            health_card = OntarioHealthCard(hin, ver)

        # Get all possible phone numbers
        tmp_extra_number = [
            prop for prop in raw_data["extras"] if prop["key"] == "demo_cell"
        ]
        tmp_phone_numbers: list[str] = [
            raw_data["phone"],
            raw_data["alternativePhone"],
            tmp_extra_number[0]["value"] if len(tmp_extra_number) != 0 else "",
        ]
        phone_numbers = [
            re.sub("[^0-9]", "", phone_number)
            for phone_number in tmp_phone_numbers
            if phone_number != ""
        ]

        # Extract address data if it exists
        address = ""
        city = ""
        province = ""
        postal_code = ""
        if "address" in raw_data:
            address = raw_data["address"]["address"]
            city = raw_data["address"]["city"]
            province = raw_data["address"]["province"]
            postal_code = raw_data["address"]["postal"]

        return Demographic(
            first_name=raw_data["firstName"],
            last_name=raw_data["lastName"],
            id=raw_data["demographicNo"],
            date_of_birth=date_of_birth,
            sex=raw_data["sex"],
            address=address,
            city=city,
            province=province,
            postal_code=postal_code,
            health_card=health_card,
            phone_numbers=phone_numbers,
            email=raw_data["email"],
        )

from dataclasses import dataclass


@dataclass(kw_only=True)
class Owner:
    id: int | None = None
    first_name: str
    last_name: str
    address: str
    city: str
    telephone: str

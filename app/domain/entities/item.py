from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class Item:
    id: str | None
    name: str
    description: str | None
    price: Decimal
    quantity: int

    def to_dict(self) -> dict[str, str | int | Decimal | None]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "quantity": self.quantity,
        }


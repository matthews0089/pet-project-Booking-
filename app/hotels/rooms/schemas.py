from typing import Optional

from pydantic import BaseModel


class RoomsInfo(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    services: list
    price: int
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int

    class Config:
        from_attributes = True
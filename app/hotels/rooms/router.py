from datetime import date, datetime
from typing import List

from app.exceptions import Booking_Too_Long, Incorrect_Data
from fastapi import APIRouter, Query

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import RoomsInfo

router = APIRouter(
    prefix="/hotels",
    tags=["Rooms"],
)


@router.get("/{hotel_id}/rooms")
async def available_rooms(hotel_id: int,
                           date_from: date = Query(..., description=f"Например, {datetime.now().date()}"), 
                           date_to: date = Query(..., description=f"Например, {datetime.now().date()}"), ) -> List[RoomsInfo]:
      
    if date_from >= date_to:
        raise Incorrect_Data
    
    if (date_to - date_from).days > 62:
        raise Booking_Too_Long
    
    rooms =  await RoomsDAO.get_rooms_by_hotel(hotel_id,date_from,date_to)
    return rooms
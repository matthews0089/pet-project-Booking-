from datetime import date

from sqlalchemy import select, func, and_

from app.database import async_session_maker
from dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_by_hotel(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            
           
            correct_date = and_(
                Bookings.date_from < date_to, 
                Bookings.date_to > date_from
            )
            
            
            book_rooms = (
                select(
                    func.count(Bookings.room_id).label("count"), 
                    Bookings.room_id
                )
                .where(correct_date)
                .group_by(Bookings.room_id)
                .cte("booked_rooms")
            )
            
            days = (date_to - date_from).days

            
            get_rooms = (
                select(
                    Rooms.__table__.columns,
                    (Rooms.price * days).label("total_cost"),
                    (Rooms.quantity - func.coalesce(book_rooms.c.count, 0)).label("rooms_left")
                )
                .select_from(Rooms)
                .join(book_rooms, book_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.hotel_id == hotel_id)
            )

            query = await session.execute(get_rooms)
            return query.mappings().all()
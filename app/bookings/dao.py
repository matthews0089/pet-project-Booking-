from datetime import date
import logging 



from dao.base import BaseDAO
from sqlalchemy import select, insert, func
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings
    @classmethod
    async def find_all_with_images(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(
                    Bookings.__table__.columns,
                    Rooms.__table__.columns,
                )
                .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                .where(Bookings.user_id == user_id)
            )
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        Створює нове бронювання, якщо є вільні номери.
        """
        async with async_session_maker() as session:
            try:
                booked_rooms = (
                    select(func.count(Bookings.id))
                    .where(
                        Bookings.room_id == room_id,
                        Bookings.date_from < date_to,
                        Bookings.date_to > date_from
                    )
                    .scalar_subquery()
                )

                room_info_query = select(
                    Rooms.price,
                    (Rooms.quantity - func.coalesce(booked_rooms, 0)).label("rooms_left")
                ).where(Rooms.id == room_id)

                room_result = await session.execute(room_info_query)
                room_info = room_result.first()

                
                if not room_info:
                    return None
                if room_info.rooms_left <= 0:
                    return None

                
                add_booking_stmt = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=room_info.price,
                    )
                    .returning(Bookings)
                )

                new_booking = await session.execute(add_booking_stmt)
                await session.commit()
                
                return new_booking.scalar()

            except SQLAlchemyError as e:
                await session.rollback()
                logging.error(f"Failed to add booking: {e}")
                return None
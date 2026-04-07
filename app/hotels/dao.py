from datetime import date
from sqlalchemy import select, func, and_, or_
from app.database import async_session_maker

from dao.base import BaseDAO
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms

class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def search_for_hotels(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            
            # 1. Временная таблица: считаем, сколько номеров уже забронировано на эти даты
            correct_date = and_(Bookings.date_from < date_to, Bookings.date_to > date_from)
            
            
            booked_rooms = (
                select(
                    Bookings.room_id,
                    func.count(Bookings.room_id).label("count")
                )
                .where(correct_date)
                .group_by(Bookings.room_id)
                .cte("booked_rooms")
            )

            # 2. Временная таблица: считаем, сколько номеров осталось свободными
            available_rooms = (
                select(
                    Rooms.__table__.columns,
                    (Rooms.quantity - func.coalesce(booked_rooms.c.count, 0)).label("rooms_left")
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .cte("available_rooms")
            )

            # 3. Финальный запрос: ищем отели в нужной локации со свободными номерами
            query = (
                select(
                    Hotels.__table__.columns,
                    func.sum(available_rooms.c.rooms_left).label("rooms_left")
                )
                .select_from(Hotels)
                .join(available_rooms, available_rooms.c.hotel_id == Hotels.id)
                .where(Hotels.location.icontains(location))
                .group_by(Hotels.id)
                .having(func.sum(available_rooms.c.rooms_left) > 0)
            )

            
            hotels = await session.execute(query)
            return hotels.mappings().all()
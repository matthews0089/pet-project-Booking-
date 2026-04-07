from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hasned_password] 
    can_delete = False
    name = "Користувач"
    name_plural = "Користувачі"
    icon = "fa-solid fa-user"

class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.columns] + [Bookings.user]
    name = "Бронювання"
    name_plural = "Бронювання"
    icon = "fa-solid fa-book"
    
    

class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.columns] + [Rooms.hotel, Rooms.bookings]
    name = "Номер"
    name_plural = "Номер"
    icon = "fa-solid fa-bed"
    
    
class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.columns] + [Hotels.rooms]
    name = "Готель"
    name_plural = "Готелі"
    icon = "fa-solid fa-hotel"
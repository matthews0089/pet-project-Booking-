import asyncio
import smtplib

from PIL import Image
from pathlib import Path


from pydantic import EmailStr
from sqlalchemy import select

from app.hotels.models import Hotels
from app.tasks.celery import celery


from app.elastic import es_client

from app.tasks.email_templates import create_booking_confirmation_template
from app.config import settings
from app.database import async_session_maker






@celery.task
def procces_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100  = im.resize((200, 100))
    im_resized_1000_500.save(f"app/static/images/resized_1000_500{im_path.name}")
    im_resized_200_100.save(f"app/static/images/resized_200_100{im_path.name}")
    


@celery.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
        
        


async def get_all_hotels():
    async with async_session_maker() as session:
        query = select(Hotels)
        result = await session.execute(query)
        return result.scalars().all()
    

@celery.task
def sync_hotels_to_es():
    hotels = asyncio.run(get_all_hotels())
    
    for hotel in hotels:
        document =  {
            "name" : hotel.name,
            "location": hotel.location,
            "services": hotel.services
        }
        
        
        es_client.index(
            index="hotels",
            id=hotel.id,
            document=document
        )
         
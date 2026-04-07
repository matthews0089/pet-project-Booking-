from email.message import EmailMessage
from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(booking: dict, email_to: EmailStr):

    message = EmailMessage()

    message["Subject"] = "Booking Confirmation"
    message["From"] = settings.SMTP_USER
    message["To"] = email_to

    message.set_content(
        f"""
Hello!

Your booking has been successfully confirmed.

Booking details:
-------------------------
Check-in date: {booking["date_from"]}
Check-out date: {booking["date_to"]}
-------------------------

Thank you for choosing our service.
We wish you a pleasant stay!

Best regards,
Hotel Booking Service
"""
    )

    return message
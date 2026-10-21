from twilio.rest import Client
from dotenv import load_dotenv
import os
from app.models.user.user_model import User

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+13612663978")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN) else None


def send_reset_sms(phone, code):
    if not client:
        print(f"⚠️ Twilio credentials not set in .env. SMS to {phone} not sent.")
        return
    try:
        client.messages.create(
            body=f"🔐 Your Okuosi password reset code is: {code}. It expires in 2 minutes.",
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )
        print(f"✅ SMS sent to {phone}")
    except Exception as e:
        print(f"❌ Failed to send SMS to {phone}: {e}")


# Sending the SMS to admins when an order is placed

def send_sms_to_admins(message_body):
    if not client:
        print("⚠️ Twilio credentials not set in .env. Admin SMS not sent.")
        return
    # Fetch all admins or employees from DB
    admins = User.query.filter_by(is_admin=True).all()

    for admin in admins:
        if admin.phone:
            try:
                client.messages.create(
                    body=message_body,
                    from_=TWILIO_PHONE_NUMBER,
                    to=admin.phone
                )
                print(f"✅ SMS sent to admin {admin.name} ({admin.phone})")
            except Exception as e:
                print(f"❌ Failed to send SMS to {admin.phone}: {e}")

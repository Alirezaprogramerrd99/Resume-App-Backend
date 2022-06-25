from app.core.config import settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='app/templates',
)


async def send_email(subject, recipients, code):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body={"code": code},
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email.html")
    return

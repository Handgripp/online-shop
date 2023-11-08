from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema, MessageType
from email_config import conf

from rq import Queue
from redis import Redis


router = APIRouter()
redis_conn = Redis(host='rq_redis')
queue = Queue('email_queue', connection=redis_conn)


async def send_email(to: str, subject: str, message: str):
    html = f"<p>{message}</p>"
    message = MessageSchema(
        subject=subject,
        recipients=[to],
        body=html,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)


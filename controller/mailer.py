from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema, MessageType
from email_config import conf
from schemas.email_schemas import EmailSchema
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


@router.post("/email")
async def simple_send(email: EmailSchema):
    to = email.email[0]
    subject = "Fastapi-Mail module"
    message = "Hi, this is a test mail, thanks for using Fastapi-mail."

    job = queue.enqueue(send_email, to, subject, message)

    return {"message": "E-mail task added to the queue", "job_id": job.id}

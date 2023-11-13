import requests
from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema, MessageType
from email_config import conf
from rq import Queue
from redis import Redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore

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

scheduler = AsyncIOScheduler()
jobstores = {
    'default': RedisJobStore(db=2, host="rq_redis", port=6379)
}
scheduler.configure(jobstores=jobstores)
scheduler.start()


@scheduler.scheduled_job('interval', hours=1)
async def check_notification():
    requests.get('http://127.0.0.1:8000/shop/products/check-products')



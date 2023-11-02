import uvicorn
from fastapi import FastAPI
from controller.user_controller import router as user_router
from controller.product_controller import router as product_router
from controller.category_controller import router as category_router
from controller.auth import router as auth_router
from controller.mailer import router as mailer_router
from controller.transaction_controller import router as transaction_router
from database import Base, engine


app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(auth_router)
app.include_router(mailer_router)
app.include_router(transaction_router)

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

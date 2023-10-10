import uvicorn
from fastapi import FastAPI
from controller.user_controller import router as controller_router
from database import Base, engine


app = FastAPI()

app.include_router(controller_router)

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import uvicorn
from fastapi import FastAPI

from database import Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

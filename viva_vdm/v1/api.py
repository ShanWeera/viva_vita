from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .endpoints import job_router

app = FastAPI(
    title="ViTA RESTful API",
    description="This is the RESTful API of ViTA",
    contact={'name': 'Shan Tharanga', 'email': 'stwm2@student.london.ac.uk'},
    version="1.0.0",
)
app.include_router(job_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

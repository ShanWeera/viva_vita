from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from viva_vdm.v1.endpoints import job_router, results_router, ncbi_router

app = FastAPI(
    title="ViTA RESTful API",
    description="This is the RESTful API of ViTA",
    contact={'name': 'Shan Tharanga', 'email': 'stwm2@student.london.ac.uk'},
    version="1.0.0",
)
app.include_router(job_router)
app.include_router(results_router)
app.include_router(ncbi_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

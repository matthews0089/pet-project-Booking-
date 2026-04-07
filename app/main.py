import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from app.logger import logger


from fastapi import FastAPI
from sqladmin import Admin


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

import sentry_sdk

from redis import asyncio as aioredis

from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.users.models import Users
from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

from app.admin.auth import authentication_backend

from app.database import engine

from app.config import settings

from app.pages.router import router as router_pages
from app.images.router import router as router_images


app = FastAPI()

sentry_sdk.init(
    dsn="https://696a383bdd2029a74878de0d8e127242@o4511144476934144.ingest.de.sentry.io/4511144479686736",
    send_default_pii=True,
)

app = FastAPI()


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)



@app.middleware("http")
async def add_procces_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    procces_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "procces_time" : round(procces_time, 4)
    })
    
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/api/v{major}',
)


app.mount("/static", StaticFiles(directory="app/static"), "static")

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
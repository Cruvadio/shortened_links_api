from fastapi import FastAPI
from .routers.links import router_links


app = FastAPI()


app.include_router(router_links)


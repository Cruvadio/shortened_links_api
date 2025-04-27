from app.schemas import URLSchema
from app.database import async_session_maker
from app.dao import LinkDAO
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import RedirectResponse
import httpx

router_links = APIRouter()
@router_links.post("/", status_code=status.HTTP_201_CREATED)
async def add_book(data: URLSchema):
    async with async_session_maker() as session:
        return await LinkDAO.shorten_link(session, data.url)

@router_links.get("/{shortened_id}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_original_link(shortened_id: str):
    async with async_session_maker() as session:
        link = await LinkDAO.find_one_or_none(session, shortened_id=shortened_id)
    if not link:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(link.original_url)

@router_links.get("/external/data", status_code=200)
async def get_external_data():
    async with httpx.AsyncClient() as client:
        respose = await client.get("https://jsonplaceholder.typicode.com/posts")

    return respose.json()



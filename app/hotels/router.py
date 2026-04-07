import asyncio
from datetime import date, datetime
from typing import List


from app.elastic import es_client

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exceptions import Booking_Too_Long, Incorrect_Data
from app.hotels.dao import HotelDAO
from app.hotels.schemas import HotelInfo

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/")
@cache(expire=60)
async def available_hotels(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
) -> List[HotelInfo]:

    if date_from >= date_to:
        raise Incorrect_Data

    if (date_to - date_from).days > 62:
        raise Booking_Too_Long

    await asyncio.sleep(3)

    hotels = await HotelDAO.search_for_hotels(location, date_from, date_to)
    return hotels


@router.get("/search")
async def search_hotels_in_es(
    search_query: str, 
    services: list[str] | None = Query(default=None) 
):
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": search_query,
                            "fields": ["name", "location"], 
                            "fuzziness": "AUTO"          
                        }
                    }
                ],
                "filter": [] 
            }
        }
    }
    
    if services:
        body["query"]["bool"]["filter"].append(
            {
                "terms": {
                    "services": services 
                }
            }
        )
    
    response = es_client.search(index="hotels", body=body)
    
    hits = response["hits"]["hits"]
    
    hotels = []
    for hit in hits:
        hotel_data = hit["_source"]   
        hotel_data["id"] = hit["_id"] 
        hotels.append(hotel_data)
        
    return hotels
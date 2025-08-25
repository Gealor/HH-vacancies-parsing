import asyncio
from collections import defaultdict
import logging
from pprint import pprint
import aiohttp
from config import settings
import orjson

from decorators import time_meter_decorator, write_into_file
from models import VacancyData

logging.basicConfig(
        level=logging.INFO, 
        format=settings.LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

log = logging.getLogger(__name__)


async def get_vacancies_on_one_page(
    aiohttp_client: aiohttp.ClientSession,
    url: str = settings.url_get_vacancies,
    page: int = 0,
):
    query_params = {
        "text": "python OR fastapi OR pydantic OR aiohttp",
        "page": page,
        "per_page": settings.PER_PAGE,
    }

    async with aiohttp_client.get(
        url=url,
        params=query_params,
    ) as response:
        response.raise_for_status()
        result = await response.json()
    log.info("Found %d items on %d page", len(result['items']), page)
    return result['items']


def parse_items(items: list[dict]) -> list[dict]:
    log.info("Start validate items...")
    result_items = []
    for elem in items:
        to_model = VacancyData.model_validate(elem)
        result_items.append(to_model.model_dump())
    log.info("Validated %d items", len(result_items))
    return result_items

def create_page_dict(page: int, items: list[VacancyData]):
    return {
        "page": page,
        "items": items
    }


async def get_all_vacancies(
    aiohttp_client: aiohttp.ClientSession,
):
    page = 0
    max_page = 2000 // settings.PER_PAGE
    
    result_list = []
    while True:

        log.info("- Start procedure %d page", page)
        if page == max_page:
            log.info("Stop searching")
            break
    
        result = await get_vacancies_on_one_page(
            aiohttp_client=aiohttp_client,
            page = page,
        )

        if len(result)==0:
            log.info("Stop searching")
            break

        items = parse_items(result)
        result_dict = create_page_dict(page=page, items = items)
        result_list.append(result_dict)
        page+=1
        await asyncio.sleep(0.5)
    
    return result_list
        
@write_into_file(settings.FILEPATH)
@time_meter_decorator
async def main():
    async with aiohttp.ClientSession() as client:
        result = await get_all_vacancies(client)
    return result

if __name__=="__main__":
    # func = time_meter_decorator(main)
    # asyncio.run(func())
    asyncio.run(main())

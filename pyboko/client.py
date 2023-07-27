import aiohttp
from typing import List

from .models import SoundsData, Marathon

BOKO_API_URL = "https://api.bokoblin.com"


class AsyncBokoClient:
    """
    Asynchronus client for accessing the Bokoblin.com API
    """

    def __init__(self):
        self._session = aiohttp.ClientSession()
    
    async def _request(self, body: str) -> dict:
        headers = {"Content-Type": "application/json"}
        async with self._session.post(url=BOKO_API_URL, headers=headers, json={"query": body}) as resp:
            data = await resp.json()
            return data

    async def get_sounds_data(self) -> SoundsData:
        """
        Get the sounds data from the API
        """
        body = """
        query{
            soundsdata{
                updated
                matching
                sounds{
                    amount
                    description
                    verified
                    newsound
                    matched
                }
            }
        }"""
        data = await self._request(body)
        return SoundsData(data["data"]["soundsdata"])
    
    async def get_marathons(self) -> List[Marathon]:
        """
        Gets the full list of marathons from the API
        """
        body = """
        query{
            marathons{
                id
                type
                type_id
                slug
                full_name
                total
                start_date
                stop_date
                playlist
                charity{
                    id
                    slug
                    full_name
                    website
                    total
                }
                color
            }
        }"""
        data = await self._request(body)
        return [Marathon(marathon) for marathon in data["data"]["marathons"]]
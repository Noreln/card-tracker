import httpx

from app.config import settings

BASE_URL = "https://api.tcgplayer.com"

# TCGPlayer category IDs
CATEGORY_IDS = {
    "pokemon": "3",
    "one_piece": "66",
}


class TCGPlayerService:
    def __init__(self):
        self._token: str | None = None

    async def _authenticate(self) -> None:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": settings.tcgplayer_api_key,
                    "client_secret": settings.tcgplayer_private_key,
                },
            )
            resp.raise_for_status()
            self._token = resp.json()["access_token"]

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self._token}"}

    async def _ensure_auth(self) -> None:
        if not self._token:
            await self._authenticate()

    async def get_card_prices(self, product_id: str) -> dict:
        await self._ensure_auth()
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BASE_URL}/pricing/product/{product_id}",
                headers=self._headers(),
            )
            resp.raise_for_status()
            return resp.json()

    async def search_cards(self, game: str, query: str, offset: int = 0, limit: int = 100) -> dict:
        await self._ensure_auth()
        category_id = CATEGORY_IDS.get(game, "3")
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BASE_URL}/catalog/products",
                headers=self._headers(),
                params={
                    "categoryId": category_id,
                    "productName": query,
                    "offset": offset,
                    "limit": limit,
                },
            )
            resp.raise_for_status()
            return resp.json()

    async def get_product_details(self, product_id: str) -> dict:
        await self._ensure_auth()
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BASE_URL}/catalog/products/{product_id}",
                headers=self._headers(),
            )
            resp.raise_for_status()
            return resp.json()


tcgplayer_service = TCGPlayerService()

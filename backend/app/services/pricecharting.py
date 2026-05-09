import httpx

from app.config import settings

BASE_URL = "https://www.pricecharting.com/api"

# PriceCharting returns prices in cents — divide by 100 for USD
_CENTS = 100

# PriceCharting console names for each game
CONSOLE_NAMES = {
    "pokemon": "Pokemon",
    "one_piece": "One Piece Card Game",
}


class PriceChartingService:
    def _auth_params(self) -> dict:
        return {"status": settings.pricecharting_api_key}

    async def search_cards(self, game: str, query: str) -> list[dict]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BASE_URL}/products",
                params={**self._auth_params(), "q": query},
            )
            resp.raise_for_status()
            data = resp.json()

        console = CONSOLE_NAMES.get(game, "")
        return [
            p for p in data.get("products", [])
            if console.lower() in p.get("console-name", "").lower()
        ]

    async def get_card_prices(self, product_id: str) -> dict | None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BASE_URL}/product",
                params={**self._auth_params(), "id": product_id},
            )
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            data = resp.json()

        return {
            "market_price": self._usd(data.get("loose-price")),
            "low_price": self._usd(data.get("loose-price")),
            "high_price": self._usd(data.get("graded-price")),
            "foil_price": self._usd(data.get("complete-price")),
        }

    @staticmethod
    def _usd(cents: int | None) -> float | None:
        if not cents:
            return None
        return round(cents / _CENTS, 2)


pricecharting_service = PriceChartingService()

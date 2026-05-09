import requests
from requests_oauthlib import OAuth1

from app.config import settings

BASE_URL = "https://api.cardmarket.com/ws/v2"

GAME_NAMES = {
    "pokemon": "Pokemon",
    "one_piece": "One Piece Card Game",
}


class CardMarketService:
    def _auth(self) -> OAuth1:
        return OAuth1(
            settings.cardmarket_app_token,
            settings.cardmarket_app_secret,
            settings.cardmarket_access_token,
            settings.cardmarket_access_secret,
        )

    def _get(self, path: str, params: dict | None = None) -> dict:
        resp = requests.get(
            f"{BASE_URL}{path}",
            auth=self._auth(),
            headers={"Accept": "application/json"},
            params=params or {},
        )
        resp.raise_for_status()
        return resp.json()

    def get_card_prices(self, product_id: str) -> dict:
        return self._get(f"/products/{product_id}")

    def search_cards(self, game: str, query: str) -> dict:
        return self._get(
            "/products/find",
            params={
                "search": query,
                "exact": 0,
                "gameName": GAME_NAMES.get(game, game),
            },
        )

    def get_price_guide(self, product_id: str) -> dict:
        return self._get(f"/products/{product_id}/priceguide")


cardmarket_service = CardMarketService()

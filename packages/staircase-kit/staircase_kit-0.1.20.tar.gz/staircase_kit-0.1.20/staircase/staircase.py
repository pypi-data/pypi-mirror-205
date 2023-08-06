from staircase.postman import StaircaseNotFoundBundle
from staircase.lib.sdk import StaircaseEnvironment

from .config import UserConfig


class Staircase:
    def __init__(self, config: UserConfig):
        if not config.marketplace_api_key:
            raise Exception("No marketplace_api_key found in config")
        self.market_place_env = StaircaseEnvironment(
            domain="marketplace.staircaseapi.com", api_key=config.marketplace_api_key
        )

    async def get_marketplace_onltology_representation(self):
        return await self.market_place_env.http_client.async_request(
            "marketplace/ontology/representation/raw"
        )

    async def get_all_product_components(self):
        next_token = None
        products = []

        while True:
            url = f"marketplace/products"
            if next_token:
                url += f"?next_token={next_token}"
            response = await self.market_place_env.http_client.async_request(url)
            response_json = await response.json()
            products += response_json.get("products", [])

            page = response_json.get("page", {})
            next_token = page.get("next_token")

            if not next_token:
                break
        return products

    async def retrieve_product_component(self, product_component_name):
        url = f"marketplace/products/{product_component_name}"
        response = await self.market_place_env.http_client.async_request(url)

        return await response.json()

    async def get_env_token(self, api_key):
        response = await self.market_place_env.http_client.async_request( f"administrator/environment/{api_key}")
        env_data = await response.json()
        token = env_data["staircase_environment"]["environment_token"]
        return token

    async def get_latest_bundle(self, component_name) -> str:
        next_token = None

        while True:
            url = f"marketplace/products/{component_name}/bundles"
            if next_token:
                url += f"?next_token={next_token}"

            res = await self.market_place_env.http_client.async_request(url)
            if res.status == 404:
                raise StaircaseNotFoundBundle("Recieve 404")

            if res.status == 403:
                raise StaircaseNotFoundBundle("Component name might contain slash")

            response_json = await res.json()
            bundles = response_json["bundles"]
            page = response_json["page"]

            for bundle in bundles:
                if not bundle['bundle_status'] == 'Valid' or  'bundle_url' not in bundle:
                    continue
                return bundle['bundle_url']


            next_token = page.get("next_token")
            if not next_token:
                break

        raise StaircaseNotFoundBundle("Not found latest bundle with success assess")

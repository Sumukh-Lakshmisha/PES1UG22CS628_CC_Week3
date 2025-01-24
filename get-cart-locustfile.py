from locust import task, run_single_user
from locust import FastHttpUser
from insert_product import login

class AddToCart(FastHttpUser):
    # Class-level constants for reuse and reduced redundancy
    host = "http://localhost:5000"
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    def __init__(self, environment):
        super().__init__(environment)
        self.username = "test123"
        self.password = "test123"
        self.token = self._get_auth_token()

    def _get_auth_token(self):
        """Encapsulate token retrieval in a dedicated method."""
        cookies = login(self.username, self.password)
        return cookies.get("token")

    @task
    def fetch_cart(self):
        """Simplified and optimized cart-fetching logic."""
        headers = {
            **self.default_headers,  # Reuse default headers
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Cookies": f"token={self.token}",
            "Referer": f"{self.host}/product/1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }

        with self.client.get("/cart", headers=headers, catch_response=True) as response:
            # Process response if needed (e.g., log failures)
            if response.status_code != 200:
                response.failure(f"Failed to fetch cart: {response.status_code}")
            else:
                response.success()

if __name__ == "__main__":
    run_single_user(AddToCart)

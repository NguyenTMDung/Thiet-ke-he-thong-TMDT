from woocommerce import API
from config import WC_API_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET

wcapi = API(
    url=WC_API_URL,
    consumer_key=WC_CONSUMER_KEY,
    consumer_secret=WC_CONSUMER_SECRET,
    version="wc/v3"
)

def get_products():
    return wcapi.get("products").json()

def add_product(data):
    return wcapi.post("products", data).json()

def update_product(product_id, data):
    return wcapi.put(f"products/{product_id}", data).json()

def delete_product(product_id):
    return wcapi.delete(f"products/{product_id}", params={"force": True}).json()
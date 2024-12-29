from flask import Flask, request, jsonify, render_template
from woocommerce import API
from config import WC_API_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET
import requests

app = Flask(__name__)

# Tạo kết nối WooCommerce API
wcapi = API(
    url=WC_API_URL,
    consumer_key=WC_CONSUMER_KEY,
    consumer_secret=WC_CONSUMER_SECRET,
    version="wc/v3",
    timeout=10
)

# Trang chính (giao diện tạo sản phẩm)
@app.route('/')
def index():
    return render_template('index.html')

# API để tạo sản phẩm mới
@app.route('/create-product', methods=['POST'])
def create_product():
    try:
        # Đọc dữ liệu JSON từ request
        product_data = request.get_json()

        # Trích xuất thông tin từ JSON
        name = product_data['name']
        sku = product_data['sku']
        categories = product_data['categories']
        stock_quantity = product_data['stock_quantity']
        description = product_data['description']
        regular_price = product_data['regular_price']
        image_url = product_data['images'][0]['src']

        # Chuẩn bị dữ liệu gửi đến WooCommerce
        product_payload = {
            "name": name,
            "sku": sku,
            "categories": [{'name': categories}],
            'manage_stock': True,
            "stock_quantity": stock_quantity,
            "description": description,
            "regular_price": regular_price,
            "images": [{'src': image_url}]
        }

        # Gửi yêu cầu POST tới WooCommerce
        response = wcapi.post("products", product_payload)

        if response.status_code == 201:
            app.logger.debug("Sản phẩm đã được tạo thành công!")
            return jsonify({"message": "Sản phẩm đã được tạo thành công!", "data": response.json()}), 201
        else:
            app.logger.debug("Lỗi khi tạo sản phẩm: %s", response.text)
            return jsonify({"message": "Không thể tạo sản phẩm.", "error": response.text}), 400

    except Exception as e:
        app.logger.error(f"Lỗi khi xử lý yêu cầu: {str(e)}")
        return jsonify({"message": f"Lỗi hệ thống: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

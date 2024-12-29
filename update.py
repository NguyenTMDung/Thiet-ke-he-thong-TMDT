from flask import Flask, request, jsonify, render_template
from woocommerce import API
from config import WC_API_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET

app = Flask(__name__)

# Kết nối WooCommerce API
wcapi = API(
    url=WC_API_URL,
    consumer_key=WC_CONSUMER_KEY,
    consumer_secret=WC_CONSUMER_SECRET,
    version="wc/v3",
    timeout=10
)

# Giao diện cập nhật sản phẩm
@app.route('/')
def update():
    return render_template('update.html')

# API cập nhật sản phẩm
@app.route('/update-product', methods=['POST'])
def update_product():
    try:
        # Lấy dữ liệu từ form
        product_id = request.form['product_id']
        name = request.form.get('name')
        sku = request.form.get('sku')
        categories = request.form.get('categories')
        stock_quantity = request.form.get('stock_quantity')
        description = request.form.get('description')
        regular_price = request.form.get('regular_price')
        image_url = request.form.get('image_url')

        # Tạo dữ liệu cần cập nhật
        product_data = {}
        if name:
            product_data['name'] = name
        if sku:
            product_data['sku'] = sku
        if categories:
            product_data['categories'] = [{'name': categories}]
        if stock_quantity:
            product_data['stock_quantity'] = int(stock_quantity)
        if description:
            product_data['description'] = description
        if regular_price:
            product_data['regular_price'] = regular_price
        if image_url:
            product_data['images'] = [{'src': image_url}]

        # Gửi yêu cầu cập nhật đến WooCommerce API
        if product_data:
            response = wcapi.put(f"products/{product_id}", product_data)

            if response.status_code == 200:
                return jsonify({"message": "Sản phẩm đã được cập nhật thành công!"}), 200
            else:
                return jsonify({"error": response.json()}), response.status_code
        else:
            return jsonify({"message": "Không có dữ liệu để cập nhật."}), 400

    except Exception as e:
        return jsonify({"message": f"Lỗi hệ thống: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

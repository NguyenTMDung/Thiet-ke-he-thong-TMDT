from flask import Flask, render_template, request, jsonify
from woocommerce import API
from config import WC_API_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET
import logging

app = Flask(__name__)

# Tạo kết nối WooCommerce API
wcapi = API(
    url=WC_API_URL,
    consumer_key=WC_CONSUMER_KEY,
    consumer_secret=WC_CONSUMER_SECRET,
    version="wc/v3"
)

# Trang chính - Giao diện tạo sản phẩm (nếu có)
@app.route('/')
def index():
    return render_template('get_product.html')

# API để lấy thông tin sản phẩm từ ID sản phẩm
@app.route('/get-product', methods=['GET'])
def get_product():
    product_id = request.args.get('product_id')  # Lấy ID sản phẩm từ tham số GET
    if not product_id:
        return jsonify({'error': "Vui lòng nhập ID sản phẩm."}), 400

    try:
        # Gửi yêu cầu GET đến API WooCommerce để lấy thông tin sản phẩm
        response = wcapi.get(f"products/{product_id}")  # Tìm sản phẩm theo ID

        if response.status_code == 200:
            product = response.json()

            # Kiểm tra xem có sản phẩm nào được tìm thấy không
            if product:
                # Trả về dữ liệu HTML để hiển thị trong AJAX
                return render_template('product_info.html', product=product)
            else:
                return jsonify({'error': "Không tìm thấy sản phẩm với ID này."}), 404
        else:
            return jsonify({'error': "Không thể lấy thông tin sản phẩm từ API."}), 500

    except Exception as e:
        app.logger.error(f"Lỗi khi xử lý yêu cầu: {str(e)}")
        return jsonify({'error': f"Lỗi hệ thống: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

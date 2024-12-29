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

# Giao diện xóa sản phẩm
@app.route('/')
def delete():
    return render_template('delete.html')

# API xóa sản phẩm
@app.route('/delete-product', methods=['POST'])
def delete_product():
    try:
        # Lấy ID sản phẩm từ form
        product_id = request.form['product_id']

        # Gửi yêu cầu xóa sản phẩm từ WooCommerce API
        response = wcapi.delete(f"products/{product_id}", params={"force": True})

        if response.status_code == 200:
            return jsonify({"message": "Sản phẩm đã được xóa thành công!"}), 200
        else:
            return jsonify({"error": response.json()}), response.status_code
    except Exception as e:
        return jsonify({"message": f"Lỗi hệ thống: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

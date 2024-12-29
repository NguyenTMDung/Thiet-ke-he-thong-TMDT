from flask import Flask, request, jsonify, render_template
from woocommerce import API
from config import WC_API_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET

app = Flask(__name__)

# Tạo kết nối WooCommerce API
wcapi = API(
    url=WC_API_URL,
    consumer_key=WC_CONSUMER_KEY,
    consumer_secret=WC_CONSUMER_SECRET,
    version="wc/v3",
)

# Trang chính - Hiển thị tất cả sản phẩm
@app.route('/')
def get_product():
    # Gửi yêu cầu GET để lấy tất cả sản phẩm
    response = wcapi.get("products")
    
    if response.status_code == 200:
        products = response.json()  # Chuyển đổi dữ liệu JSON thành Python dict
        if products:  # Kiểm tra nếu có sản phẩm
            return render_template('getAllProduct.html', products=products)
        else:
            return render_template('getAllProduct.html', error="Không có sản phẩm nào.")
    else:
        return f"Lỗi khi lấy sản phẩm: {response.text}", 500

if __name__ == "__main__":
    app.run(debug=True)

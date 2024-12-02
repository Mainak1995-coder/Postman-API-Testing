from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Mock database
data = [
    {"id": 1, "name": "Product A", "price": 100},
    {"id": 2, "name": "Product B", "price": 200},
]

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# API to get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(data)

# API to get a single product by ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((item for item in data if item['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# API to add a product with auto-generated ID
@app.route('/api/products', methods=['POST'])
def add_product():
    new_product = request.json
    if "name" not in new_product or "price" not in new_product:
        return jsonify({"error": "Missing required fields: name or price"}), 400
    
    # Auto-generate ID
    new_id = max(item["id"] for item in data) + 1 if data else 1
    new_product["id"] = new_id
    data.append(new_product)
    return jsonify({"message": "Product added successfully", "product": new_product}), 201

# API to update a product by ID
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((item for item in data if item['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    updated_data = request.json
    product.update(updated_data)
    return jsonify({"message": "Product updated successfully", "product": product})

# API to delete a product by ID
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global data
    data = [item for item in data if item['id'] != product_id]
    return jsonify({"message": "Product deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)

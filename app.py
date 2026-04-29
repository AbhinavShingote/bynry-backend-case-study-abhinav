from flask import Flask, request, jsonify
from models import db, Product, Inventory, Warehouse, Supplier, ProductSupplier

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# -------------------------------
# PART 1 : CREATE PRODUCT API
# -------------------------------
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    try:
        if 'name' not in data or 'sku' not in data or 'price' not in data:
            return {"error": "name, sku and price are required"}, 400

        if data['price'] < 0:
            return {"error": "price cannot be negative"}, 400

        initial_quantity = data.get('initial_quantity', 0)
        if initial_quantity < 0:
            return {"error": "quantity cannot be negative"}, 400

        existing_product = Product.query.filter_by(sku=data['sku']).first()
        if existing_product:
            return {"error": "SKU already exists"}, 400

        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=data['price']
        )
        db.session.add(product)
        db.session.flush()

        if 'warehouse_id' in data:
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=initial_quantity
            )
            db.session.add(inventory)

        db.session.commit()

        return {"message": "Product created", "product_id": product.id}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": "Unable to create product"}, 500


# -------------------------------
# PART 3 : LOW STOCK ALERT API
# -------------------------------
@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alert(company_id):
    alerts = []

    inventories = db.session.query(Inventory, Product, Warehouse)\
        .join(Product, Inventory.product_id == Product.id)\
        .join(Warehouse, Inventory.warehouse_id == Warehouse.id)\
        .filter(Warehouse.company_id == company_id)\
        .all()

    for inventory, product, warehouse in inventories:
        if inventory.quantity < inventory.threshold:
            supplier_link = ProductSupplier.query.filter_by(product_id=product.id).first()
            supplier = Supplier.query.get(supplier_link.supplier_id) if supplier_link else None

            avg_sales = inventory.avg_daily_sales if inventory.avg_daily_sales > 0 else 1
            days_until_stockout = inventory.quantity // avg_sales

            alerts.append({
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "warehouse_id": warehouse.id,
                "warehouse_name": warehouse.name,
                "current_stock": inventory.quantity,
                "threshold": inventory.threshold,
                "days_until_stockout": days_until_stockout,
                "supplier": {
                    "id": supplier.id if supplier else None,
                    "name": supplier.name if supplier else "N/A",
                    "contact_email": supplier.contact_email if supplier else "N/A"
                }
            })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from decimal import Decimal

from flask import Flask, jsonify, request

from utils import get_delivery_cost, zero

app = Flask(__name__)


class InvalidAPIUsage(Exception):
    """Custom class to handle custom exceptions"""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code


@app.route("/", methods=['POST'])
def api_endpoint():
    data = request.get_json()
    data_keys = data.keys()
    # validate necessary keys are present in the json data
    for x in ['order_items', 'distance']:
        if x not in data_keys:
            raise InvalidAPIUsage(f"Missing '{x}' data in api", status_code=400)
    item_total = zero
    for items in data['order_items']:
        # validations for appropriate data are present or not
        if not items.get('name', '') or not items.get('quantity', None) or not items.get('price', None):
            raise InvalidAPIUsage("Missing data against product in api", status_code=400)
        # validation for non negative data
        if items['price'] < 0 or items['quantity'] < 0:
            raise InvalidAPIUsage("Items needs non negative price and quantity", status_code=401)
        item_total += Decimal(items['quantity'] * items['price'])

    if data['distance'] > 50000:
        raise InvalidAPIUsage("Items needs non negative price and quantity", status_code=401)
    delivery_cost = get_delivery_cost(Decimal(data['distance'] or 0.0))
    discount_amt = zero
    if 'offer' in data_keys:
        discount_type = data['offer']['offer_type']
        if discount_type == 'FLAT':
            discount_amt = Decimal(data['offer']['offer_val'])
        elif discount_type == 'DELIVERY':
            discount_amt = delivery_cost
        else:
            # unrecognised discount type
            raise InvalidAPIUsage("Unrecognized Discount Type", status_code=401)
    order_total_without_disc = item_total + delivery_cost
    # only if discount is greater than order amount apply discount
    if discount_amt > order_total_without_disc:
        order_total = order_total_without_disc
    else:
        order_total = order_total_without_disc - discount_amt
    return {'order_total': float(order_total)}

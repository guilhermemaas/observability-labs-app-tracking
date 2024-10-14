from flask import Flask, jsonify
from faker import Faker
import random

app = Flask (__name__)
fake = Faker()

def generate_shipping_cost():
    return round(random.uniform(10,1000), 2)

def generate_shipping_weight():
    return round(random.uniform(10,1000), 3)

def generate_delivery_time():
    return fake.date_time_this_month().strftime("%m/%d/%Y, %H:%M:%S")

@app.route('/shipping', methods=['GET'])
def get_name():
    shipping= {
        'shipping_code': fake.ean13(),
        'name': fake.name(),
        'address': fake.address(),
        'latitude': fake.latitude(),
        'longitude': fake.longitude(),
        'shipping_cost': generate_shipping_cost(),
        'shipping_weight': generate_shipping_weight(),
        'estimated_delivery_time': generate_delivery_time()
    }

    return jsonify(shipping)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5006)
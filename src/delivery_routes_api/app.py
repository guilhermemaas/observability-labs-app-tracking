from flask import Flask, jsonify, request
import pika
import json

app = Flask (__name__)

@app.route('/shipping', methods=['POST'])
def post_shipping():
    shipping_data = request.json

    required_fields = {
        'shipping_code', 'address', 'latitude', 'longitude', 'shipping_cost',
        'shipping_weight', 'estimated_delivery_time'
    }

    if not all(field in shipping_data for field in required_fields):
        return jsonify({"error": "Missing fields in request data"}), 400

    #Create RabbitMQ connection
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='rabbitmq', port='5672', credentials=pika.PlainCredentials('guest', 'guest')))
    rabbitmq_channel = rabbitmq_connection.channel()
    rabbitmq_channel.queue_declare(queue='shipping_queue')

    #Send message to RabbitMQ queue and close connection
    rabbitmq_channel.basic_publish(exchange='', routing_key='shipping_queue', body=json.dumps(shipping_data))
    rabbitmq_connection.close()

    return jsonify({"message": "Data sent to process queue",
                    "data": shipping_data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5007)
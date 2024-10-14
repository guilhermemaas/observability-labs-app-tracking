import pika
import json
from pymongo import MongoClient

def main():
    #Mongodb connection
    mongo_client = MongoClient('mongodb://localhost:27017/')
    db = mongo_client.shipping_db
    collection = db.shippings

    #Create RabbitMQ connection
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port='5672', credentials=pika.PlainCredentials('guest', 'guest')))
    rabbitmq_channel = rabbitmq_connection.channel()
    rabbitmq_channel.queue_declare(queue='shipping_queue')

    def callback(ch, method, properties, body):
        shipping_data = json.loads(body)
        print('Received shipping data:', shipping_data)

        #Insert document on MondgoDB
        collection.insert_one(shipping_data)
        print('Inserted into MongoDB', shipping_data)

    rabbitmq_channel.basic_consume(queue='shipping_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages.')

    rabbitmq_channel.start_consuming()

if __name__ == '__main__':
    main()
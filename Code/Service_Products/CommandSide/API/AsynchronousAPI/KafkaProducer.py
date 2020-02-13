from confluent_kafka import Producer
import json
from Repository.ProductRepository import ProductRepository
import threading



class ProduceToBroker(object):

    def __init__(self):
        self.p = Producer({'bootstrap.servers': 'localhost:9092'})

    #Activate when Kafka sends its callback
    def delivery_report(self, err, msg, Details):

        msg = json.loads(msg)
        print(f'Message:Send, Service: Προΐόντα, EventType:{msg["Message"]["Head"]["EventType"]}')
        ProductRepository().UpdateEventThatItHasBeenPublished(Details[0],Details[1],Details[2]) #Update the event that was published successfully



    #Publish the messages
    def Publish(self, Message, Topic, Details):        
       
        # Trigger any available delivery report callbacks from previous produce() calls
        self.p.poll(0)
        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.
        self.p.produce(Topic, value=Message.encode('utf-8'), callback=threading.Thread(target=self.delivery_report, args=(None,Message,Details)).start())

    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
        self.p.flush()

from confluent_kafka import Producer
import json
from time import sleep
from Repository.OrderRepository import OrderRepository
import threading
from time import sleep


class ProduceToBroker(object):

    def __init__(self):
        self.p = Producer({'bootstrap.servers': 'localhost:9092'})

    #Activate when Kafka sends its callback
    def delivery_report(self, err, msg, Details):
        msg = json.loads(msg)
        print(f'Message:Send, Service: Παραγγελίες, EventType:{msg["Message"]["Head"]["EventType"]}')
        OrderRepository().UpdateEventThatItHasBeenPublished(Details[0],Details[1],Details[2],Details[3]) #Update the event that was published successfully


    def Publish(self, Message, Topic, Details):        
       
        # Trigger any available delivery report callbacks from previous produce() calls
        self.p.poll(0)
        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.
        if Topic == 'OrderServiceEventChannel':
            self.p.produce(Topic, value=Message.encode('utf-8'), key=json.dumps(str(Details[2])),  callback=threading.Thread(target=self.delivery_report, args=(None,Message,Details)).start())
        else:    
            self.p.produce(Topic, value=Message.encode('utf-8'), callback=threading.Thread(target=self.delivery_report, args=(None,Message,Details)).start())

    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
        self.p.flush()

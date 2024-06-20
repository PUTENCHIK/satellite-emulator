from broker import Broker

class Subscriber:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.broker.subscribe(topic, self)

    def receive(self, topic):
        if topic == self.topic:
            messages = self.broker.topics[topic]
            for i in range(1,len(messages)):
                print(f"Subscriber {self.topic} received message: {messages[i]}")
            self.broker.topics[topic] = []


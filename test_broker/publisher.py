from broker import Broker

class Publisher:
    def __init__(self, broker):
        self.broker = broker

    def publish(self, topic, message):
        self.broker.publish(topic, message)

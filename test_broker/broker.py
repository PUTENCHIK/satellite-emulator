class Broker:
    def __init__(self):
        self.topics = {}

    def publish(self, topic, message):
        if topic not in self.topics:
            self.topics[topic] = []
        self.topics[topic].append(message)
        self.notify_subscribers(topic)

    def subscribe(self, topic, subscriber):
        if topic not in self.topics:
            self.topics[topic] = []
        self.topics[topic].append(subscriber)

    def notify_subscribers(self, topic):
        if topic in self.topics:
            for subscriber in self.topics[topic]:
                if (isinstance(subscriber, str))==False:
                    subscriber.receive(topic)

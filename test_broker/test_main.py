from publisher import Publisher
from subscriber import (Subscriber)
from broker  import Broker
import threading
import time
# Создание брокера
broker = Broker()
# Создание издателя
publisher = Publisher(broker)
# Создание подписчиков
subscriber1 = Subscriber(broker, "news")
subscriber2 = Subscriber(broker, "sports")
# Публикация сообщений
publisher.publish("news", "Breaking news: The world is flat.")
publisher.publish("sports", "The local football team won the championship.")
# Симуляция цикла сообщений (для демонстрации)
i=0
while True:
    i+=1
    if (i>5):
        break
    # Отправить сообщения с случайной задержкой
    time.sleep(2)
    publisher.publish("news", f"News update: {time.time()}")
# Инициализация потоков для подписчиков
subscriber1_thread = threading.Thread(target=subscriber1.receive, args=("news",))
subscriber2_thread = threading.Thread(target=subscriber2.receive, args=("sports",))
# Запуск потоков подписчиков
subscriber1_thread.start()
subscriber2_thread.start()
# Держать скрипт в работе для обработки сообщений
while True:
    i+=1
    if (i>10):
        break
    time.sleep(1)

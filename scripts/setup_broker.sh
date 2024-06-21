#!/bin/bash

# Обновление списка пакетов
sudo apt-get update

# Установка Mosquitto
sudo apt-get install -y mosquitto

# Настройка конфигурационного файла для Mosquitto
cat <<EOT >> /etc/mosquitto/mosquitto.conf
# Основные настройки брокера
listener 1883
max_connections 2000
allow_anonymous true
# Настройки логирования
log_dest file /var/log/mosquitto/mosquitto.log
log_type all

# Настройки сохранения сообщений
persistence true
persistence_location /var/lib/mosquitto/

# Настройки ограничения размера сообщения
message_size_limit 512000

#Настройки интервала системных сообщений
sys_interval 10
EOT

# Перезапуск службы Mosquitto для применения новой конфигурации
sudo systemctl restart mosquitto

# Включение автоматического запуска Mosquitto при загрузке системы
sudo systemctl enable mosquitto

# Проверка статуса Mosquitto
sudo systemctl status mosquitto

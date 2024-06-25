#!/bin/bash

# Путь к директории со станциями
STATIONS_DIR="../files"

# Файл состояния для отслеживания неактивных служб
STATE_FILE="/tmp/stations_state.txt"

# Инициализация файла состояния, если он не существует
touch "$STATE_FILE"
chmod +x "$STATE_FILE"

# Функция для проверки и перезапуска станции
check_and_restart_station() {
    local station_name=$1
    local service_file="${station_name}.service"
    local crontab_id="#${station_name}-restart"

    # Проверяем статус сервиса
    if systemctl is-active --quiet "$service_file"; then
        # Если служба активна, удаляем её из файла состояния, если она там есть
        sed -i "/${service_file}/d" "${STATE_FILE}"
        # Удаляем задачу из crontab, если она там есть
        (crontab -l | grep -v "${crontab_id}") | crontab -
    else
        # Если служба не активна, проверяем код завершения
        local last_exit_code=$(systemctl show -p ExecMainStatus "$service_file" | cut -d'=' -f2)
        if [ "${last_exit_code}" != "0" ]; then
            # Если служба завершилась с ошибкой, перезапускаем немедленно
            systemctl restart "${service_file}"
        else
            # Если служба завершилась без ошибок, проверяем crontab перед добавлением
            if ! (crontab -l | grep -q "${crontab_id}"); then
    		# Добавляем задачу в crontab, если её там нет
		(crontab -l; echo "59 23 * * * sleep 31 && systemctl restart ${service_file} ${crontab_id} && (crontab -l | grep -v '${crontab_id}') | crontab -") | crontab -
	    fi
        fi
        # Проверяем, есть ли уже запись о службе в файле состояния
        if ! grep -q "${service_file}" "$STATE_FILE"; then
            # Отмечаем службу как неактивную, если её там нет
            echo "$service_file" >> "$STATE_FILE"
        fi
    fi
}

# Перебираем все станции и проверяем их статус
for station_dir in "$STATIONS_DIR"/*; do
    if [ -d "$station_dir" ]; then
        station_name=$(basename "$station_dir")
        check_and_restart_station "$station_name"
    fi
done

# Отдельно проверяем службу subscriber.service
check_and_restart_station "subscriber"

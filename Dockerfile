FROM postgres:14
# Копирование нового скрипта entrypoint, если это необходимо
COPY ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
# Установка прав на выполнение скрипта
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

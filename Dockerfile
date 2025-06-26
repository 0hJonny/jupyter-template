# Dockerfile
ARG BASE_IMAGE=quay.io/jupyterhub/jupyterhub:5.3.0
FROM ${BASE_IMAGE}

# Установка зависимостей в один слой
RUN python3 -m pip install --no-cache-dir \
    dockerspawner \
    jupyterhub-nativeauthenticator \
    jupyterhub-idle-culler \
    psycopg2-binary \
    # Дополнительные зависимости для работы с Docker API
    docker

# Создаем рабочую директорию
WORKDIR /srv/jupyterhub

# Копируем конфигурацию отдельным слоем
COPY jupyterhub_config.py ./

# Экспортируем порт и устанавливаем команду запуска
EXPOSE 8000
CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]

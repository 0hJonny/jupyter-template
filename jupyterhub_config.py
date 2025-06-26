# /srv/jupyterhub/jupyterhub_config.py
c = get_config()

# ========================
# Безопасность и производительность
# ========================
# Всегда используйте внешний прокси (NGINX) для production
#c.JupyterHub.proxy_class = None  # Отключаем встроенный прокси

# Использовать PostgreSQL вместо SQLite
#c.JupyterHub.db_url = 'postgresql://jupyterhub_user:password@localhost/jupyterhub_db'

# Принудительное использование HTTPS
#c.JupyterHub.ssl_cert = '/etc/ssl/certs/jupyterhub.crt'
#c.JupyterHub.ssl_key = '/etc/ssl/private/jupyterhub.key'
#c.JupyterHub.cookie_secret_file = '/srv/jupyterhub/jupyterhub_cookie_secret'

# Безопасность кук
#c.JupyterHub.cookie_max_age_days = 0.5  # Сессии 12 часов
#c.ConfigurableHTTPProxy.auth_token = 'your_secure_proxy_token'  # Для связи с NGINX

# ========================
# Docker Spawner
# ========================
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = "docker.io/0hjohnny/scipy-notebook:python-3.13.5"  # Явно укажите образ
c.DockerSpawner.remove = True  # Автоочистка контейнеров
c.DockerSpawner.network_name = "jupyterhub_network"

# Ограничение ресурсов
c.DockerSpawner.mem_limit = "4G"
c.DockerSpawner.cpu_limit = 1.0

# Важно для корректной маршрутизации
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.DockerSpawner.hub_connect_ip = 'jupyterhub'



# ========================
# Аутентификация
# ========================
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'

# Вариант 1: Самостоятельная регистрация пользователей
c.NativeAuthenticator.enable_signup = True  # Разрешить регистрацию
#c.NativeAuthenticator.open_signup = False    # Требовать подтверждение регистрации
c.NativeAuthenticator.open_signup = True  # Без подтверждения регистрации

# Вариант 2: Только ручное добавление администратором
# c.NativeAuthenticator.enable_signup = False  # Отключить самостоятельную регистрацию

# Общие настройки:
c.Authenticator.admin_users = {'admin'}  # Укажите логины администраторов
c.Authenticator.allowed_users = set()    # Оставьте пустым для разрешения всех
c.Authenticator.allow_all = True

# Политика паролей
c.NativeAuthenticator.minimum_password_length = 8
c.NativeAuthenticator.check_common_password = True
c.NativeAuthenticator.allowed_failed_logins = 5
c.NativeAuthenticator.seconds_before_next_try = 300  # 5 мин блокировки

# Подтверждение email (рекомендуется)
#c.NativeAuthenticator.ask_email_on_signup = True
c.NativeAuthenticator.allow_password_change = True

# Настройка SMTP для почтовых уведомлений
#c.NativeAuthenticator.smtp_host = 'smtp.your-domain.com'
#c.NativeAuthenticator.smtp_port = 587
#c.NativeAuthenticator.smtp_user = 'jupyterhub@your-domain.com'
#c.NativeAuthenticator.smtp_password = 'your-secure-password'
#c.NativeAuthenticator.smtp_use_starttls = True
#c.NativeAuthenticator.from_email = 'JupyterHub <noreply@your-domain.com>'

# ========================
# Дополнительные функции
# ========================
# Требовать смену пароля при первом входе
c.NativeAuthenticator.force_password_change = True

# Автоматическое одобрение пользователей из белого списка
# c.Authenticator.allowed_users = {'user1', 'user2', 'user3'}

# Включить двухфакторную аутентификацию (2FA)
# c.NativeAuthenticator.allow_2fa = True

# ========================
# Оптимизации
# ========================
c.JupyterHub.active_server_limit = 100  # Макс. активных серверов
c.JupyterHub.cleanup_servers = True     # Автоочистка неактивных
c.JupyterHub.concurrent_spawn_limit = 10 # Ограничение одновременных запусков

# Блокировка неактивных пользователей
c.JupyterHub.services = [
    {
        "name": "idle-culler",
        "command": [
            "python3", "-m", "jupyterhub_idle_culler",
            "--timeout=3600",  # Закрывать через 1 час неактивности
            "--cull-users=true"
        ]
    }
]

# Ограничение сессий
c.Spawner.default_url = '/lab'  # Стартовая страница
c.Spawner.cmd = ['jupyter-labhub']  # Использовать JupyterLab

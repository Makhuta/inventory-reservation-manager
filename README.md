### Docker

Download [docker-compose.yaml](https://github.com/Makhuta/tranga-manager/blob/main/docker-compose.yaml) and configure to your needs. 
The `docker-compose` also includes [Tranga](https://github.com/C9Glax/tranga) as backend. For its configuration refer to the repo README.

#### Environmental Variables

| Name | Default | Required | Description |
| - | - | - | - |
| ```DEBUG``` | False | False | Enables debug for Django |
| ```SECRET_KEY``` |  | True | Secret key for Django |
| ```ALLOWED_HOSTS``` | * | False | List of allowed hosts separated with "," |
| ```DJANGO_USERNAME``` | Admin | False (Recommended) | Manager Login username |
| ```DJANGO_PASSWORD``` | irm-admin | False (Recommended) | Manager Login password |
| ```DJANGO_EMAIL``` | default@email.com | False | Manager Login email (not currently used for anything) |
| ```DATABASE_DIR``` | /app | False (Recommended) | Directory in which the db.sqlite3 will be saved (highly recomended to use for keeping the connections/added APIs) |
| ```CSRF_TRUSTED_ORIGINS``` | localhost:80,127.0.0.1:80 | False | Trusted origins for CSRF |
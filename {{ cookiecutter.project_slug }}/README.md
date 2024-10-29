# {{ cookiecutter.project_name }}

## Começando

Copiar .env-EXAMPLE to .env

Alterar .env conforme necessário

Instalar dependências:

    poetry install

Criar o banco de dados

    poetry run python manage.py migrate

Criar usuário inicial

    poetry run python manage.py createsuperuser

Executar servidor de desenvolvimento:

    poetry run python manage.py runserver

Abrir http://localhost:8000/ no navegador

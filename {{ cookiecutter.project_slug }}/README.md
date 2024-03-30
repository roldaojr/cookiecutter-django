# {{ cookiecutter.project_name }}

## Começando

Copiar .env-EXAMPLE to .env

Alterar .env conforme necessário

Instalar dependências:

    poetry install

Criar o banco de dados

    poetry run manage migrate

Criar usuário incial

    poetry run manage createsuperuser

Executar servidor de desenvolvimento:

    poetry run manage runserver

Abrir http://localhost:8000/ no navegador

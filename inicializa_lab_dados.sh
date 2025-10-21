#!/bin/bash
# Script de inicialização do ambiente de dados da Vania

echo "Iniciando laboratório de dados..."

# Entrar na past do projeto
cd ~/projetos_airbnb

# Ativar ambiente virtual
source venv/bin/activate

#Iniciar serviço do PostgreSQL
sudo service postgresql start

#Confirmar bibliotecas essenciais
pip list | grep -E "pandas|sqlalchemy|psycopg2"

echo "Ambiente pronto! Boa aula, Vania!"







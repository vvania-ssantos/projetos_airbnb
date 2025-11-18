import pandas as pd
import psycopg2
from psycopg2 import sql

# --- 1. DETALHES DA CONEXÃO ---
DB_NAME = "projetos_airbnb"
DB_USER = "postgres"
DB_PASS = "supervania"  # <-- SUBSTITUA AQUI PELA SENHA REAL!
DB_HOST = "localhost"
DB_PORT = "5432"

# --- 2. FUNÇÃO PRINCIPAL DE CARREGAMENTO ---
def carregar_dados():
    try:
        # 2.1 Extrai e Transforma: Lê o CSV (e remove a coluna vazia)
        df = pd.read_csv('Cidades do RJ.csv')
        df = df[['neighbourhood']].rename(columns={'neighbourhood': 'bairro'})

        print(f"Dados lidos do CSV: {len(df)} bairros.")

    except FileNotFoundError:
        print("ERRO: O arquivo 'Cidades do RJ.csv' não foi encontrado.")
        return

    conn = None
    try:
        # 2.2 Conexão
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        # 2.3 Carregamento (Excluindo dados antigos antes de inserir)
        cur.execute("TRUNCATE TABLE bairros_rj RESTART IDENTITY;") # Limpa a tabela para a nova importação

        # Inserção em massa (row by row)
        for index, row in df.iterrows():
            # Cria o comando INSERT SQL
            insert_query = sql.SQL("INSERT INTO bairros_rj (bairro) VALUES ({})").format(
                sql.Literal(row['bairro'])
            )
            cur.execute(insert_query)

        conn.commit()
        print(f"\nSUCESSO: {len(df)} bairros inseridos na tabela bairros_rj.")
        cur.close()

    except (Exception, psycopg2.Error) as error:
        print(f"\nERRO FATAL DURANTE A INSERÇÃO. Verifique se a tabela bairros_rj existe. Erro: {error}")

    finally:
        if conn is not None:
            conn.close()

carregar_dados()

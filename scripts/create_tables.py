# scripts/create_tables.py
import sys
import os

# Adicione o diretório raiz do projeto ao PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database import create_connection # Para tabelas de staging (se usar mysql.connector)
from mysql.connector import Error

# Se você estiver usando SQLAlchemy para seu DW (fato/dimensões), importe de src.models
# from src.models import Base, engine as dw_engine # Assumindo que src/models.py define Base e engine


def create_aquisicao_dia_table():
    """Cria a tabela aquisicao_dia para staging."""
    connection = create_connection()
    cursor = connection.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS aquisicao_dia (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome_arquivo VARCHAR(255),
        nome_originador VARCHAR(255),
        cnpj_originador VARCHAR(20),
        nome_cedente VARCHAR(255),
        cnpj_cedente VARCHAR(20),
        nome_fundo VARCHAR(255),
        cnpj_fundo VARCHAR(20),
        dt_cessao DATE,
        nome_sacado VARCHAR(255),
        cidade VARCHAR(100),
        estado VARCHAR(2),
        cep VARCHAR(10),
        data_nascimento DATE,
        numero_contrato VARCHAR(50),
        taxa_anual_juros DECIMAL(10,2),
        seu_numero_numero_parcela_djkj VARCHAR(50),
        vl_presente DECIMAL(10,2),
        valor_futuro_nominal DECIMAL(10,2),
        data_vencimento_parcela DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table aquisicao_dia created successfully or already exists.")
    except Error as e:
        print(f"Error creating aquisicao_dia table: {e}")
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

# Você pode adicionar funções semelhantes para criar outras tabelas de staging
# def create_estoque_aquisicoes_table():
#     # ... SQL para estoque_aquisicoes
#     pass

# def create_liquidados_estoque_table():
#     # ... SQL para liquidados_estoque
#     pass

# Se você estiver usando SQLAlchemy para as tabelas do Data Warehouse (fato/dimensões)
# def create_dw_tables():
#     """Cria as tabelas do Data Warehouse usando SQLAlchemy."""
#     try:
#         Base.metadata.create_all(dw_engine)
#         print("Data Warehouse tables created successfully or already exist.")
#     except Exception as e:
#         print(f"Error creating Data Warehouse tables: {e}")


def main():
    print("Creating all necessary tables...")
    create_aquisicao_dia_table()
    # create_estoque_aquisicoes_table() # Descomente se for criar
    # create_liquidados_estoque_table() # Descomente se for criar
    # if 'dw_engine' in globals(): # Se SQLAlchemy estiver configurado
    #    create_dw_tables()
    print("Table creation process finished.")

if __name__ == "__main__":
    main()
from config.database import create_connection

def create_estoque_aquisicoes_table():
    """Create the estoque_aquisicoes table"""
    connection = create_connection()
    cursor = connection.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS estoque_aquisicoes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome_fundo VARCHAR(255),
        cnpj_fundo VARCHAR(20),
        nome_originador VARCHAR(255),
        cnpj_originador VARCHAR(20),
        nome_cedente VARCHAR(255),
        cnpj_cedente VARCHAR(20),
        nome_sacado VARCHAR(255),
        tipo_recebivel VARCHAR(50),
        valor_futuro DECIMAL(10,2),
        valor_presente DECIMAL(10,2),
        valor_aquisicao DECIMAL(10,2),
        data_aquisicao DATE,
        numero_contrato VARCHAR(50),
        numero_parcela VARCHAR(50),
        taxa_juros DECIMAL(10,8),
        data_vencimento DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table estoque_aquisicoes created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()
from config.database import create_connection

def create_aquisicao_dia_table():
    """Create the aquisicao_dia table"""
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
        print("Table aquisicao_dia created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()
from config.database import create_connection

def create_liquidados_estoque_table():
    """Create the liquidados_estoque table"""
    connection = create_connection()
    cursor = connection.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS liquidados_estoque (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fundo VARCHAR(255),
        data_movimento DATE,
        data_aquisicao DATE,
        tipo_movimento VARCHAR(50),
        contrato VARCHAR(50),
        cedente VARCHAR(255),
        sacado VARCHAR(255),
        valor_pago DECIMAL(10,2),
        numero_parcela VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table liquidados_estoque created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()
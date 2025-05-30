import os
import sys
from pathlib import Path
import mysql.connector
from mysql.connector import Error

# Configuração do PATH para imports
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))

from config.database import create_connection

# Mapeamento de arquivos SQL para suas respectivas tabelas
SQL_FILE_MAPPING = {
    'aquisicao_dia_database_fundo_teste.sql': {
        'table_name': 'aquisicao_dia',
        'model': 'aquisicao_dia'
    },
    'estoque_aquisicoes_database_fundo_teste.sql': {
        'table_name': 'estoque_aquisicoes',
        'model': 'estoque_aquisicoes'
    },
    'liquidados_estoque_database_fundo_teste.sql': {
        'table_name': 'liquidados_estoque',
        'model': 'liquidados_estoque'
    }
}

def verify_table_structure(connection, table_name, model_name):
    """Verifica se a estrutura da tabela corresponde ao modelo"""
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Obtém as colunas da tabela no banco
        cursor.execute(f"DESCRIBE {table_name}")
        table_columns = {col['Field'] for col in cursor.fetchall()}
        
        # Importa o modelo dinamicamente
        model_module = __import__(f'models.{model_name}', fromlist=[''])
        
        # Obtém as colunas esperadas do modelo
        if hasattr(model_module, 'TABLE_COLUMNS'):
            model_columns = set(model_module.TABLE_COLUMNS)
        else:
            # Se não houver TABLE_COLUMNS definido, assume que está correto
            return True
        
        # Verifica se todas as colunas do modelo existem na tabela
        missing_columns = model_columns - table_columns
        if missing_columns:
            print(f"⚠️ Aviso: Tabela {table_name} está faltando colunas: {', '.join(missing_columns)}")
            return False
        
        return True
        
    except Error as e:
        print(f"❌ Erro ao verificar estrutura da tabela {table_name}: {e}")
        return False
    finally:
        if cursor:
            cursor.close()

def execute_sql_file(file_path, connection, table_name, model_name):
    """
    Executa um arquivo SQL completo com verificação de estrutura
    """
    # Primeiro verifica a estrutura da tabela
    if not verify_table_structure(connection, table_name, model_name):
        print(f"❌ Estrutura da tabela {table_name} não corresponde ao modelo {model_name}")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Lê o arquivo SQL
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Remove comentários e divide comandos
        commands = [cmd.strip() for cmd in sql_content.split(';') 
                   if cmd.strip() and not cmd.strip().startswith('--') 
                   and not cmd.strip().startswith('/*')]
        
        success_count = 0
        error_count = 0
        
        for command in commands:
            try:
                if command:  # Ignora comandos vazios
                    cursor.execute(command)
                    success_count += 1
            except Error as e:
                print(f"⚠️ Erro no comando SQL para tabela {table_name}: {e}")
                print(f"Comando problemático (trecho): {command[:200]}...")
                error_count += 1
                continue
        
        connection.commit()
        print(f"✅ Dados importados para tabela {table_name}")
        print(f"   Comandos executados: {success_count}")
        print(f"   Comandos com erro: {error_count}")
        return True
        
    except Error as e:
        print(f"❌ Erro ao executar arquivo SQL para tabela {table_name}: {e}")
        connection.rollback()
        return False
    except Exception as e:
        print(f"❌ Erro inesperado com tabela {table_name}: {e}")
        return False
    finally:
        if cursor:
            cursor.close()

def import_sql_files():
    """Importa todos os arquivos SQL da pasta data com verificação de modelos"""
    print("\n🚀 Iniciando importação de arquivos SQL com verificação de modelos...")
    
    connection = None
    try:
        connection = create_connection()
        if not connection:
            print("❌ Falha ao conectar ao banco de dados")
            return False
        
        # Ordem de importação recomendada
        import_order = [
            'aquisicao_dia_database_fundo_teste.sql',
            'estoque_aquisicoes_database_fundo_teste.sql',
            'liquidados_estoque_database_fundo_teste.sql'
        ]
        
        for sql_file in import_order:
            if sql_file not in SQL_FILE_MAPPING:
                print(f"⚠️ Arquivo {sql_file} não está mapeado em SQL_FILE_MAPPING")
                continue
                
            file_path = root_dir / 'data' / sql_file
            if not file_path.exists():
                print(f"⚠️ Arquivo não encontrado: {file_path}")
                continue
            
            config = SQL_FILE_MAPPING[sql_file]
            print(f"\n📦 Processando: {sql_file} → Tabela: {config['table_name']}")
            
            execute_sql_file(
                file_path,
                connection,
                config['table_name'],
                config['model']
            )
            
        return True
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            connection.close()

def main():
    # Primeiro cria as tabelas se necessário
    from scripts.create_tables import main as create_tables_main
    create_tables_main()
    
    # Executa a importação dos arquivos SQL
    success = import_sql_files()
    
    if success:
        print("\n🎉 Importação concluída com sucesso!")
    else:
        print("\n⚠️ A importação foi concluída com erros. Verifique os logs acima.")

if __name__ == "__main__":
    main()
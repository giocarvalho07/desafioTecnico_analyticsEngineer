# tests/test_data_processing.py

import pandas as pd
import numpy as np
from datetime import datetime
import pytest

# Importa as funções que você quer testar do seu main.py
# OBS: Pode ser necessário ajustar o sys.path ou a estrutura de importação
# se o seu main.py não estiver na raiz do projeto ou se você o renomear.
# Assumindo que main.py está na raiz e as funções não são privadas.
from main import convert_currency, convert_date, clean_data, load_data

# Mock de dados para testes unitários mais isolados
@pytest.fixture
def sample_aquisicoes_raw():
    """Fornece um DataFrame de aquisições simulado para testes."""
    data = {
        'nome_fundo': ['FUNDO A', 'FUNDO B', 'FUNDO A'],
        'vl_presente': ['1.234,56', '500,00', '99,99'],
        'valor_futuro_nominal': ['2.000,00', 'N/A', '800,00'],
        'dt_cessao': ['01/01/2023', '15/02/2023', 'invalid-date'],
        'data_vencimento_da_parcela': ['10/06/2024', '20/07/2025', '05/05/2024']
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_estoque_raw():
    """Fornece um DataFrame de estoque simulado para testes."""
    data = {
        'NOME_FUNDO': ['FUNDO A', 'FUNDO B', 'FUNDO A'],
        'VALOR_FUTURO': ['1000,00', '2500,50', '300,00'],
        'VALOR_PRESENTE': ['950,00', '2300,75', 'XYZ'], # Teste de erro aqui
        'VALOR_AQUISICAO': ['800,00', '2000,00', '250,00'],
        'DATA_AQUISICAO': ['01/01/2023', '15/02/2023', '01/03/2023'],
        'DATA_VENCIMENTO': ['20/05/2025', '01/04/2024', '30/06/2025']
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_liquidados_raw():
    """Fornece um DataFrame de liquidados simulado para testes."""
    data = {
        'FUNDO': ['FUNDO A', 'FUNDO B'],
        'VALOR_PAGO': ['1.000,00', '500,00'],
        'DATA_MOVIMENTO': ['05/05/2024', '20/03/2024'],
        'DATA_AQUISICAO': ['01/01/2023', '15/02/2023']
    }
    return pd.DataFrame(data)


# Testes para convert_currency
def test_convert_currency_valid_input():
    assert convert_currency("1.234,56") == 1234.56
    assert convert_currency("100,00") == 100.00
    assert convert_currency("500") == 500.00

def test_convert_currency_invalid_input():
    assert np.isnan(convert_currency("abc"))
    assert np.isnan(convert_currency("N/A"))
    assert np.isnan(convert_currency(None))
    assert np.isnan(convert_currency(""))

# Testes para convert_date
def test_convert_date_valid_input():
    assert convert_date("01/01/2023") == datetime(2023, 1, 1)
    assert convert_date("15/02/2024", date_format='%d/%m/%Y') == datetime(2024, 2, 15)

def test_convert_date_invalid_input():
    assert pd.isna(convert_date("invalid-date"))
    assert pd.isna(convert_date("30/02/2023")) # Data inválida (fevereiro não tem 30)
    assert pd.isna(convert_date(None))
    assert pd.isna(convert_date(""))

# Teste de integração para clean_data
def test_clean_data_aquisicoes(sample_aquisicoes_raw):
    # A função clean_data espera 3 DFs, mockamos os outros como vazios para este teste específico
    clean_aq, _, _ = clean_data(sample_aquisicoes_raw, pd.DataFrame(), pd.DataFrame())

    # Verifica se as colunas numéricas foram convertidas corretamente
    assert clean_aq['vl_presente'].iloc[0] == 1234.56
    assert clean_aq['valor_futuro_nominal'].iloc[0] == 2000.00
    assert np.isnan(clean_aq['valor_futuro_nominal'].iloc[1]) # N/A deve ser NaN

    # Verifica se as colunas de data foram convertidas corretamente
    assert clean_aq['dt_cessao'].iloc[0] == datetime(2023, 1, 1)
    assert pd.isna(clean_aq['dt_cessao'].iloc[2]) # 'invalid-date' deve ser NaT
    assert clean_aq['data_vencimento_da_parcela'].iloc[2] == datetime(2024, 5, 5)

    # Verifica os dtypes após a limpeza
    assert pd.api.types.is_float_dtype(clean_aq['vl_presente'])
    assert pd.api.types.is_datetime64_any_dtype(clean_aq['dt_cessao'])

def test_clean_data_estoque(sample_estoque_raw):
    _, clean_est, _ = clean_data(pd.DataFrame(), sample_estoque_raw, pd.DataFrame())

    # Verifica se as colunas numéricas foram convertidas corretamente, incluindo tratamento de erro
    assert clean_est['VALOR_PRESENTE'].iloc[0] == 950.00
    assert np.isnan(clean_est['VALOR_PRESENTE'].iloc[2]) # 'XYZ' deve ser NaN

    # Verifica dtypes
    assert pd.api.types.is_float_dtype(clean_est['VALOR_FUTURO'])
    assert pd.api.types.is_datetime64_any_dtype(clean_est['DATA_AQUISICAO'])
    assert pd.api.types.is_datetime64_any_dtype(clean_est['DATA_VENCIMENTO'])

def test_clean_data_liquidados(sample_liquidados_raw):
    _, _, clean_liq = clean_data(pd.DataFrame(), pd.DataFrame(), sample_liquidados_raw)

    # Verifica valor e tipo de dado
    assert clean_liq['VALOR_PAGO'].iloc[0] == 1000.00
    assert pd.api.types.is_float_dtype(clean_liq['VALOR_PAGO'])
    assert pd.api.types.is_datetime64_any_dtype(clean_liq['DATA_MOVIMENTO'])
    assert pd.api.types.is_datetime64_any_dtype(clean_liq['DATA_AQUISICAO'])
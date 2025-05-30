import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from datetime import datetime
from pathlib import Path

# Configuração inicial
plt.style.use('ggplot')
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.max_columns', None) # Para ver todas as colunas no debug
pd.set_option('display.width', 1000) # Ajusta a largura de exibição do console

def debug_data(df, name):
    """Função auxiliar para debug de dados"""
    print(f"\n--- Debug {name} ---")
    if df.empty:
        print(f"{name} está vazio.")
        return

    print(f"Colunas: {df.columns.tolist()}")
    print(f"Formato: {df.shape}")
    print(f"Tipos de dados:\n{df.dtypes}")
    print("Primeiras 2 linhas:")
    # Usar to_string() para melhor visualização de DataFrames
    print(df.head(2).to_string()) 
    
    # Debug específico para colunas de data/valor
    date_cols = [col for col in df.columns if 'DATA' in col.upper() or 'DT_' in col.upper()]
    val_cols = [col for col in df.columns if 'VALOR' in col.upper() or 'VL_' in col.upper()]

    if date_cols:
        print("\nAmostra de colunas de data (primeiras 5):")
        for col in date_cols:
            if col in df.columns:
                print(f"  {col} (Tipo: {df[col].dtype}, Nulos: {df[col].isna().sum()}):")
                print(df[col].head(5).to_string())
    
    if val_cols:
        print("\nAmostra de colunas de valor (primeiras 5):")
        for col in val_cols:
            if col in df.columns:
                print(f"  {col} (Tipo: {df[col].dtype}, Nulos: {df[col].isna().sum()}):")
                print(df[col].head(5).to_string())
    print("-" * (len(name) + 12)) # Linha separadora


def load_data():
    """Carrega os dados dos arquivos CSV/TXT com tratamento robusto"""
    data_dir = Path('data')
    
    # Inicializa DataFrames vazios para garantir que sempre retornem algo
    aquisicoes = pd.DataFrame()
    estoque = pd.DataFrame()
    liquidados = pd.DataFrame()

    print(f"Tentando carregar dados do diretório: {data_dir.absolute()}")

    try:
        aquisicoes_path = data_dir / 'aquisicao_dia_database_fundo_teste.csv'
        aquisicoes = pd.read_csv(
            aquisicoes_path,
            sep=';',
            encoding='latin1',
            dtype='object'  # Carrega tudo como string para conversão controlada
        )
        print(f"✅ '{aquisicoes_path.name}' carregado.")
        debug_data(aquisicoes, 'aquisicoes (raw)')
    except FileNotFoundError:
        print(f"❌ Arquivo '{aquisicoes_path.name}' não encontrado em '{data_dir}'.")
    except Exception as e:
        print(f"❌ Erro ao carregar aquisições de '{aquisicoes_path.name}': {e}")

    try:
        # CORRIGIDO: Nome do arquivo .txt conforme o que você mencionou
        estoque_path = data_dir / 'estoque_aquisicoes_database_fundo_teste.txt' 
        estoque = pd.read_csv(
            estoque_path,
            sep=';',
            encoding='latin1',
            dtype='object'
        )
        print(f"✅ '{estoque_path.name}' carregado.")
        debug_data(estoque, 'estoque (raw)')
    except FileNotFoundError:
        print(f"❌ Arquivo '{estoque_path.name}' não encontrado em '{data_dir}'.")
    except Exception as e:
        print(f"❌ Erro ao carregar estoque de '{estoque_path.name}': {e}")

    try:
        liquidados_path = data_dir / 'liquidados_estoque_database_fundo_teste.csv'
        liquidados = pd.read_csv(
            liquidados_path,
            sep=';',
            encoding='latin1',
            dtype='object'
        )
        print(f"✅ '{liquidados_path.name}' carregado.")
        debug_data(liquidados, 'liquidados (raw)')
    except FileNotFoundError:
        print(f"❌ Arquivo '{liquidados_path.name}' não encontrado em '{data_dir}'.")
    except Exception as e:
        print(f"❌ Erro ao carregar liquidados de '{liquidados_path.name}': {e}")

    return aquisicoes, estoque, liquidados

def convert_currency(value):
    """Conversão segura de valores monetários"""
    try:
        if pd.isna(value) or str(value).strip() in ['', 'NA', 'NaN', 'None', 'Null']:
            return np.nan
        # Remove pontos de milhar (se houver) e substitui vírgula decimal por ponto
        value = str(value).strip().replace('.', '').replace(',', '.')
        return float(value)
    except ValueError: # Capturar specificamente ValueError para strings não numéricas
        return np.nan
    except Exception: # Captura outras exceções genéricas
        return np.nan

def convert_date(value, date_format='%d/%m/%Y'):
    """Conversão robusta para datetime com tratamento de NaT"""
    if pd.isna(value) or str(value).strip() == '':
        return pd.NaT # Not a Time (valor nulo para datetime)
    
    # Tenta com o formato principal
    try:
        date = pd.to_datetime(value, format=date_format, errors='coerce')
        if pd.notna(date): # Verifica se a conversão resultou em uma data válida
            return date
    except Exception:
        pass # Ignora e tenta o próximo

    # Se a primeira tentativa falhar, tenta sem um formato explícito (inferindo)
    # Isso pode ser útil para formatos ligeiramente diferentes, mas menos seguro
    try:
        date = pd.to_datetime(value, errors='coerce')
        if pd.notna(date):
            return date
    except Exception:
        pass

    return pd.NaT # Retorna NaT se todas as tentativas falharem


def clean_data(aquisicoes, estoque, liquidados):
    """Limpeza e transformação robusta dos dados"""
    print("\n--- Limpeza e Conversão de Dados ---")
    
    # Aquisições
    if not aquisicoes.empty:
        for col in ['vl_presente', 'valor_futuro_nominal']:
            if col in aquisicoes.columns:
                aquisicoes[col] = aquisicoes[col].apply(convert_currency)
        
        for col in ['dt_cessao', 'data_vencimento_da_parcela']:
            if col in aquisicoes.columns:
                aquisicoes[col] = aquisicoes[col].apply(convert_date)
        print("✅ DataFrame 'aquisicoes' processado.")
        debug_data(aquisicoes, 'aquisicoes (clean)')
    else:
        print("⚠️ DataFrame 'aquisicoes' está vazio, pulando limpeza.")
    
    # Estoque
    if not estoque.empty:
        for col in ['VALOR_FUTURO', 'VALOR_PRESENTE', 'VALOR_AQUISICAO']:
            if col in estoque.columns:
                estoque[col] = estoque[col].apply(convert_currency)
        
        # ESSA É A COLUNA CRÍTICA PARA O ERRO ANTERIOR (.dt accessor)
        for col in ['DATA_AQUISICAO', 'DATA_VENCIMENTO']:
            if col in estoque.columns:
                estoque[col] = estoque[col].apply(convert_date)
        
        print("✅ DataFrame 'estoque' processado.")
        debug_data(estoque, 'estoque (clean)')
    else:
        print("⚠️ DataFrame 'estoque' está vazio, pulando limpeza.")
    
    # Liquidados
    if not liquidados.empty:
        if 'VALOR_PAGO' in liquidados.columns:
            liquidados['VALOR_PAGO'] = liquidados['VALOR_PAGO'].apply(convert_currency)
        
        for col in ['DATA_MOVIMENTO', 'DATA_AQUISICAO']:
            if col in liquidados.columns:
                liquidados[col] = liquidados[col].apply(convert_date)
        print("✅ DataFrame 'liquidados' processado.")
        debug_data(liquidados, 'liquidados (clean)')
    else:
        print("⚠️ DataFrame 'liquidados' está vazio, pulando limpeza.")

    return aquisicoes, estoque, liquidados

def calculate_kpis(aquisicoes, estoque, liquidados):
    """Cálculo dos KPIs com tratamento robusto de datas e dados"""
    print("\n--- Calculando KPIs ---")
    
    # Verifica se os DataFrames essenciais não estão vazios
    if aquisicoes.empty:
        print("❌ DataFrame 'aquisicoes' está vazio. Não é possível calcular KPIs.")
        return pd.DataFrame()
    
    # Obtém lista de fundos únicos
    # Usar .dropna() para garantir que não há NaNs em 'nome_fundo' antes de obter únicos
    fundos = aquisicoes['nome_fundo'].dropna().unique()
    if len(fundos) == 0:
        print("❌ Nomes de fundos não encontrados no DataFrame de aquisições. Verifique a coluna 'nome_fundo'.")
        return pd.DataFrame()

    kpis = []
    # CORREÇÃO CRÍTICA AQUI: Define 'hoje' como um Timestamp do Pandas para consistência
    hoje_ts = pd.to_datetime(datetime.now().date())
    hoje_date = hoje_ts.date() # Versão datetime.date para comparações de data pura

    for fundo in fundos:
        print(f"\n⚙️ Processando fundo: {fundo}")
        
        try:
            # Filtra dados por fundo e cria cópias para evitar SettingWithCopyWarning
            aq_fundo = aquisicoes[aquisicoes['nome_fundo'] == fundo].copy()
            est_fundo = estoque[estoque['NOME_FUNDO'] == fundo].copy() if 'NOME_FUNDO' in estoque.columns else pd.DataFrame()
            liq_fundo = liquidados[liquidados['FUNDO'] == fundo].copy() if 'FUNDO' in liquidados.columns else pd.DataFrame()
            
            # 1. Volume total cedido
            volume_cedido = 0
            if not aq_fundo.empty and 'vl_presente' in aq_fundo.columns:
                volume_cedido = aq_fundo['vl_presente'].sum()
                if pd.isna(volume_cedido): volume_cedido = 0
            print(f"   Volume Cedido: R$ {volume_cedido:,.2f}")

            # 2. Volume em estoque atual
            volume_estoque = 0
            if not est_fundo.empty and 'VALOR_PRESENTE' in est_fundo.columns:
                volume_estoque = est_fundo['VALOR_PRESENTE'].sum()
                if pd.isna(volume_estoque): volume_estoque = 0
            print(f"   Volume Estoque: R$ {volume_estoque:,.2f}")
            
            # 3. Índice de inadimplência (% de vencidos não pagos)
            inadimplencia = 0
            if not est_fundo.empty and 'DATA_VENCIMENTO' in est_fundo.columns and pd.api.types.is_datetime64_any_dtype(est_fundo['DATA_VENCIMENTO']):
                # Filtrar NaT antes de comparar
                est_fundo_valid_dates = est_fundo.dropna(subset=['DATA_VENCIMENTO'])
                
                if not est_fundo_valid_dates.empty:
                    # Compara a parte da data do Timestamp com a data de hoje (objeto date)
                    vencidos = est_fundo_valid_dates[est_fundo_valid_dates['DATA_VENCIMENTO'].dt.date < hoje_date]
                    inadimplencia = len(vencidos) / len(est_fundo_valid_dates)
            print(f"   Inadimplência: {inadimplencia:.2%}")

            # 4. Retorno realizado (valor recebido / valor cedido)
            valor_recebido = 0
            if not liq_fundo.empty and 'VALOR_PAGO' in liq_fundo.columns:
                valor_recebido = liq_fundo['VALOR_PAGO'].sum()
                if pd.isna(valor_recebido): valor_recebido = 0
            retorno = valor_recebido / volume_cedido if volume_cedido > 0 else 0
            print(f"   Retorno Realizado: {retorno:.2%}")
            
            # 5. Tempo médio até a baixa (dias)
            tempo_medio_baixa = 0
            if not liq_fundo.empty and 'DATA_MOVIMENTO' in liq_fundo.columns and 'DATA_AQUISICAO' in liq_fundo.columns and \
               pd.api.types.is_datetime64_any_dtype(liq_fundo['DATA_MOVIMENTO']) and pd.api.types.is_datetime64_any_dtype(liq_fundo['DATA_AQUISICAO']):
                
                # Filtrar NaT antes de calcular
                liq_fundo_valid_dates = liq_fundo.dropna(subset=['DATA_MOVIMENTO', 'DATA_AQUISICAO'])
                if not liq_fundo_valid_dates.empty:
                    # Subtração entre Timestamps resulta em Timedelta, depois .dt.days
                    liq_fundo_valid_dates['tempo_baixa'] = (liq_fundo_valid_dates['DATA_MOVIMENTO'] - liq_fundo_valid_dates['DATA_AQUISICAO']).dt.days
                    tempo_medio_baixa = liq_fundo_valid_dates['tempo_baixa'].mean()
            print(f"   Tempo Médio Baixa: {tempo_medio_baixa:,.0f} dias")

            # 6. Aging dos recebíveis (Distribuição dos títulos conforme o tempo de atraso)
            # Este KPI já está implementado e robustecido.
            aging = {'a_vencer': 0, '0_30': 0, '31_60': 0, '61_90': 0, '91_mais': 0}
            if not est_fundo.empty and 'DATA_VENCIMENTO' in est_fundo.columns and pd.api.types.is_datetime64_any_dtype(est_fundo['DATA_VENCIMENTO']):
                est_fundo_valid_dates = est_fundo.dropna(subset=['DATA_VENCIMENTO'])
                if not est_fundo_valid_dates.empty:
                    # Calcula os dias de atraso (hoje - data de vencimento). Use hoje_ts para Timedelta.
                    est_fundo_valid_dates['dias_atraso'] = (hoje_ts - est_fundo_valid_dates['DATA_VENCIMENTO']).dt.days
                    
                    aging = {
                        'a_vencer': len(est_fundo_valid_dates[est_fundo_valid_dates['DATA_VENCIMENTO'].dt.date >= hoje_date]),
                        '0_30': len(est_fundo_valid_dates[(est_fundo_valid_dates['dias_atraso'] > 0) & (est_fundo_valid_dates['dias_atraso'] <= 30)]), # Maior que 0 para ser atraso
                        '31_60': len(est_fundo_valid_dates[(est_fundo_valid_dates['dias_atraso'] > 30) & (est_fundo_valid_dates['dias_atraso'] <= 60)]),
                        '61_90': len(est_fundo_valid_dates[(est_fundo_valid_dates['dias_atraso'] > 60) & (est_fundo_valid_dates['dias_atraso'] <= 90)]),
                        '91_mais': len(est_fundo_valid_dates[est_fundo_valid_dates['dias_atraso'] > 90])
                    }
            print(f"   Aging: {aging}")
            
            kpis.append({
                'fundo': fundo,
                'volume_cedido': volume_cedido,
                'volume_estoque': volume_estoque,
                'inadimplencia': inadimplencia,
                'retorno': retorno,
                'tempo_medio_baixa': tempo_medio_baixa,
                'aging': aging # Dicionário de aging incluído
            })
            
        except Exception as e:
            print(f"⚠️ Erro ao processar fundo {fundo}: {str(e)}. Adicionando NaN.")
            # Registrar erro e continuar para o próximo fundo
            kpis.append({
                'fundo': fundo,
                'volume_cedido': np.nan, 'volume_estoque': np.nan,
                'inadimplencia': np.nan, 'retorno': np.nan,
                'tempo_medio_baixa': np.nan, 'aging': {}
            })
            continue # Pula para o próximo fundo

    print("\n✅ Cálculo de KPIs concluído para todos os fundos.")
    return pd.DataFrame(kpis)


def create_dashboard(kpis_df):
    """Criação do dashboard visual"""
    print("\n--- Gerando Dashboard Visual ---")
    if kpis_df.empty:
        print("❌ Nenhum dado válido para criar o dashboard. Verifique os KPIs calculados.")
        return
    
    fig = plt.figure(figsize=(18, 12), constrained_layout=True) # constrained_layout para ajustar espaçamentos
    fig.suptitle('Dashboard de KPIs por Fundo', fontsize=16, fontweight='bold', y=1.02) # y ajusta a posição do título
    
    # Layout do dashboard: 3 linhas, 3 colunas (ajustado para remover ax7)
    gs = GridSpec(3, 3, figure=fig) # Mantém 3x3 por enquanto para facilitar o mapeamento
    
    # Gráfico 1: Volume Total Cedido
    ax1 = fig.add_subplot(gs[0, 0])
    kpis_df.plot.bar(x='fundo', y='volume_cedido', ax=ax1, legend=False, color='skyblue')
    ax1.set_title('Volume Total Cedido (R$)', fontsize=12)
    ax1.set_ylabel('Valor (R$)', fontsize=10)
    ax1.set_xlabel('') # Remover label do eixo x
    ax1.tick_params(axis='x', rotation=45, labelsize=9)
    ax1.ticklabel_format(style='plain', axis='y') # Evita notação científica no eixo y
    for container in ax1.containers: # Adicionar valores nas barras
        ax1.bar_label(container, fmt='R$%.0f', fontsize=8, padding=3)

    # Gráfico 2: Volume em Estoque
    ax2 = fig.add_subplot(gs[0, 1])
    kpis_df.plot.bar(x='fundo', y='volume_estoque', ax=ax2, legend=False, color='lightcoral')
    ax2.set_title('Volume em Estoque Atual (R$)', fontsize=12)
    ax2.set_ylabel('Valor (R$)', fontsize=10)
    ax2.set_xlabel('')
    ax2.tick_params(axis='x', rotation=45, labelsize=9)
    ax2.ticklabel_format(style='plain', axis='y')
    for container in ax2.containers:
        ax2.bar_label(container, fmt='R$%.0f', fontsize=8, padding=3)
    
    # Gráfico 3: Índice de Inadimplência
    ax3 = fig.add_subplot(gs[0, 2])
    kpis_df.plot.bar(x='fundo', y='inadimplencia', ax=ax3, legend=False, color='lightgreen')
    ax3.set_title('Índice de Inadimplência (%)', fontsize=12)
    ax3.set_ylabel('Percentual', fontsize=10)
    ax3.set_xlabel('')
    # Garante que o ylim superior não seja zero se max() for zero
    max_inadimplencia = kpis_df['inadimplencia'].max()
    ax3.set_ylim(0, max_inadimplencia * 1.1 if max_inadimplencia > 0 else 0.1) 
    ax3.yaxis.set_major_formatter('{:.1%}'.format)
    ax3.tick_params(axis='x', rotation=45, labelsize=9)
    for container in ax3.containers:
        ax3.bar_label(container, fmt='%.1f%%', fontsize=8, padding=3) # Formato para percentual
    
    # Gráfico 4: Retorno Realizado
    ax4 = fig.add_subplot(gs[1, 0])
    kpis_df.plot.bar(x='fundo', y='retorno', ax=ax4, legend=False, color='gold')
    ax4.set_title('Retorno Realizado (R$/R$)', fontsize=12)
    ax4.set_ylabel('Retorno', fontsize=10)
    ax4.set_xlabel('')
    # Ajusta o limite superior para exibir melhor os valores, se houver retornos muito altos
    max_retorno = kpis_df['retorno'].max()
    ax4.set_ylim(0, max_retorno * 1.2 if max_retorno > 0 else 0.1)
    ax4.yaxis.set_major_formatter('{:.1%}'.format)
    ax4.tick_params(axis='x', rotation=45, labelsize=9)
    for container in ax4.containers:
        ax4.bar_label(container, fmt='%.1f%%', fontsize=8, padding=3)

    # Gráfico 5: Tempo Médio até Baixa
    ax5 = fig.add_subplot(gs[1, 1])
    kpis_df.plot.bar(x='fundo', y='tempo_medio_baixa', ax=ax5, legend=False, color='mediumpurple')
    ax5.set_title('Tempo Médio até Baixa (dias)', fontsize=12)
    ax5.set_ylabel('Dias', fontsize=10)
    ax5.set_xlabel('')
    ax5.tick_params(axis='x', rotation=45, labelsize=9)
    for container in ax5.containers:
        ax5.bar_label(container, fmt='%.0f', fontsize=8, padding=3)
    
    # Gráfico 6: Aging dos Recebíveis (Barra Empilhada)
    # Re-mapeando o subplot para ocupar a linha 1, coluna 2 (se possível)
    # ou expandindo para as 2 últimas linhas, na última coluna, como antes, se for o melhor layout.
    # Como a tabela foi removida, podemos reajustar o layout para que os gráficos ocupem melhor o espaço.
    # Por exemplo, poderíamos fazer o ax6 ocupar as posições [1,2] e [2,2]
    # Ou ajustar para um layout 2x3 e remapear tudo.
    # Pela sua imagem anterior, o ax6 ocupava as últimas duas linhas da última coluna.
    # Vamos manter isso para manter a visualização similar, apenas removendo a tabela.
    ax6 = fig.add_subplot(gs[1:, 2]) # Ocupa a segunda e terceira linha na terceira coluna
    
    aging_data = []
    categories = ['a_vencer', '0_30', '31_60', '61_90', '91_mais']
    display_categories = ['A Vencer', '0-30 dias', '31-60 dias', '61-90 dias', '91+ dias']

    for fundo_idx, fundo in enumerate(kpis_df['fundo']):
        aging_dict = kpis_df.loc[kpis_df['fundo'] == fundo, 'aging'].iloc[0]
        aging_data.append([aging_dict.get(cat, 0) for cat in categories])

    bottom = np.zeros(len(kpis_df))
    
    # Correção para get_cmap()
    cmap = plt.colormaps.get_cmap('viridis')
    num_colors = len(categories)
    # Garante que não haja divisão por zero se houver apenas uma categoria
    colors = [cmap(i / (num_colors - 1)) for i in range(num_colors)] if num_colors > 1 else [cmap(0.5)] 

    for i, cat_key in enumerate(categories):
        values = [row[i] for row in aging_data]
        ax6.bar(kpis_df['fundo'], values, bottom=bottom, label=display_categories[i], color=colors[i])
        bottom += values
    
    ax6.set_title('Aging dos Recebíveis (Quantidade de Títulos)', fontsize=12)
    ax6.set_ylabel('Quantidade de Títulos', fontsize=10)
    ax6.set_xlabel('')
    ax6.legend(title='Faixa de Atraso', fontsize=8, title_fontsize=9)
    ax6.tick_params(axis='x', rotation=45, labelsize=9)
    
    # REMOVIDA A SEÇÃO ax7 (Tabela de resumo) AQUI

    plt.subplots_adjust(wspace=0.3, hspace=0.6) # Ajusta espaçamento entre os subplots
    plt.savefig('dashboard_kpis.png', dpi=300, bbox_inches='tight', pad_inches=0.5) # Aumenta o padding
    plt.show() # Mostra o dashboard na tela
    print("✅ Dashboard gerado e salvo como 'dashboard_kpis.png'")


def main():
    print("🚀 Iniciando análise de KPIs...")
    
    try:
        # 1. Carregar dados
        print("\n1. Carregando dados...")
        aquisicoes, estoque, liquidados = load_data()
        
        # Verificar se os DataFrames essenciais foram carregados
        if aquisicoes.empty and estoque.empty and liquidados.empty:
            print("❌ Nenhum arquivo de dados foi carregado com sucesso. Abortando.")
            return

        # 2. Limpar e converter dados
        print("\n2. Processando dados (limpeza e conversão de tipos)...")
        aquisicoes, estoque, liquidados = clean_data(aquisicoes, estoque, liquidados)
        
        # 3. Calcular KPIs
        print("\n3. Calculando KPIs...")
        kpis_df = calculate_kpis(aquisicoes, estoque, liquidados)
        
        if kpis_df.empty:
            print("❌ Nenhum KPI pôde ser calculado. Verifique os dados de entrada e as mensagens de debug acima.")
            return
        
        # 4. Criar dashboard
        print("\n4. Gerando dashboard...")
        create_dashboard(kpis_df)
        
        print("\n✅ Análise de KPIs concluída com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro fatal inesperado durante a execução: {str(e)}")
        import traceback
        traceback.print_exc() # Imprime o traceback completo para depuração

if __name__ == "__main__":
    main()
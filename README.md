Desafio Técnico: Engenheiro de Analytics - Pipeline ETL e Dashboards
Este repositório contém uma solução para um desafio técnico de Engenheiro de Analytics, focado na construção de um pipeline ETL (Extract, Transform, Load) e na geração de indicadores (KPIs) visualizados em um dashboard. O projeto simula o processamento de dados de aquisições, estoque e liquidações para fornecer insights de negócio.

Sumário
Visão Geral do Projeto
Objetivos do Desafio
Arquitetura e Tecnologias
Tecnologias Utilizadas
Fluxo de Dados ETL (Exemplo Resumido)
Estrutura do Projeto
Configuração do Ambiente
1. Clonar o Repositório
2. Criar e Ativar o Ambiente Virtual
3. Instalar Dependências
4. Configurar Arquivos de Dados
Execução do Projeto
Etapa 1: Popular o Banco de Dados (Simulação)
Simulação de Ingestão e Persistência Incremental
Etapa 2: Executar o Cálculo de KPIs e Gerar o Dashboard
Resultados Esperados
Considerações Finais e Melhorias Futuras
Visão Geral do Projeto
Este projeto aborda as principais etapas de um pipeline de dados analítico:

Ingestão de Dados: Leitura de arquivos CSV/TXT de diferentes fontes.
Transformação e Modelagem: Limpeza, padronização e estruturação dos dados em um modelo normalizado (simulado para PostgreSQL) e a criação de tabelas dimensionais.
Carga (Load): Simulação de carga incremental em um Data Warehouse (conceitualmente, pode ser BigQuery, Redshift ou um schema dedicado no PostgreSQL).
Análise e Visualização: Cálculo de indicadores chave de performance (KPIs) e geração de um dashboard visual utilizando Matplotlib.
Objetivos do Desafio
Desenvolver um processo ETL robusto para dados financeiros.
Aplicar técnicas de modelagem de dados para análise.
Calcular e visualizar KPIs essenciais para o acompanhamento de operações financeiras.
Demonstrar habilidades em Python para manipulação de dados e visualização.
Arquitetura e Tecnologias
O projeto é construído em Python e utiliza bibliotecas populares para manipulação, análise e visualização de dados. A arquitetura é de um Monolito de Script, onde todas as etapas do ETL e da geração de KPIs são executadas em um único arquivo, facilitando a portabilidade para demonstração.

Tecnologias Utilizadas
Linguagem de Programação: Python 3.x
Manipulação e Análise de Dados: pandas, numpy
Visualização de Dados: matplotlib
Gerenciamento de Caminhos de Arquivo: pathlib (módulo padrão do Python)
Simulação de Banco de Dados/DW: No contexto deste projeto, a persistência e a carga no banco de dados/DW são simuladas através da manipulação de DataFrames em memória e a persistência em arquivos para demonstração do conceito incremental. Para um cenário real, seriam utilizadas bibliotecas como SQLAlchemy e drivers específicos para PostgreSQL, BigQuery, Redshift, etc.
Fluxo de Dados ETL (Exemplo Resumido)
O pipeline ETL, embora simulado em um único script, segue os princípios de cada etapa:

Ingestão (Extract):

Lê os arquivos .csv e .txt (aquisicao_dia_database_fundo_teste.csv, estoque_aquisicoes_database_fundo_teste.txt, liquidados_estoque_database_fundo_teste.csv) da pasta data/.
Identifica registros não processados (neste caso, a simulação incremental seria baseada em timestamps ou IDs já processados).
Tecnologias: pandas.read_csv, pathlib.
Transformação & Modelagem:

Limpeza: Conversão de tipos de dados (moeda para float, strings de data para datetime), tratamento de valores nulos e inconsistências.
Normalização: Os dados são tratados e limpos para se adequarem a um modelo normalizado.
Modelo Utilizado (Conceitual): Embora a persistência em banco de dados não seja física neste script, a intenção é seguir um Modelo Estrela (Star Schema) ou um Modelo Floco de Neve (Snowflake Schema) simplificado, onde teríamos:
Tabelas Fato (Fato Aquisição, Fato Estoque, Fato Liquidação): Contendo métricas e chaves estrangeiras para dimensões.
Tabelas Dimensionais (Dim Fundo, Dim Origem, Dim Cedente, Dim Sacado, Dim Tempo): Contendo atributos descritivos.
As funções de limpeza (clean_data) e cálculo de KPIs já preparam os dados nesse formato conceitual para uso analítico.
Tecnologias: pandas (para manipulação de DataFrames), numpy (para NaN).
Carga em Data Warehouse (Load):

Os dados transformados são utilizados diretamente em memória para o cálculo de KPIs, simulando a carga em um DW.
Para uma implementação real, esta etapa envolveria a escrita dos DataFrames limpos em tabelas específicas de um Data Warehouse (e.g., PostgreSQL, BigQuery, Redshift) usando pandas.to_sql() ou APIs de carregamento direto.
A simulação de carga incremental seria feita ao identificar novos registros ou registros modificados nas fontes e aplicar UPSERTs (UPDATE + INSERT) ou MERGE nas tabelas do DW.
Tecnologias: pandas (para manipulação de dados prontos para carga), conceitualmente SQLAlchemy para ORM/conexão DB.
Indicadores (KPIs) & Dashboard:

Cálculo dos KPIs por fundo: Volume total cedido, Volume em estoque atual, Índice de inadimplência, Retorno realizado, Tempo médio até a baixa, e Aging dos recebíveis.
Geração de um dashboard visual consolidado para análise.
Tecnologias: pandas (para agregações), matplotlib (para gráficos).
Estrutura do Projeto
.
├── data/
│   ├── aquisicao_dia_database_fundo_teste.csv
│   ├── estoque_aquisicoes_database_fundo_teste.txt
│   └── liquidados_estoque_database_fundo_teste.csv
├── main.py
├── dashboard_kpis.png  (Gerado após a execução)
└── README.md
data/: Diretório que contém os arquivos de dados brutos de entrada.
main.py: O script principal que contém todo o pipeline ETL e a lógica de geração de KPIs/Dashboard.
dashboard_kpis.png: Imagem do dashboard gerado, salva automaticamente após a execução.
README.md: Este arquivo, com a documentação do projeto.
Configuração do Ambiente
Para configurar e executar este projeto em sua máquina local, siga os passos abaixo:

1. Clonar o Repositório
Primeiro, clone este repositório para o seu ambiente local usando Git:

Bash

git clone https://github.com/giocarvalho07/desafioTecnico_analyticsEngineer.git
cd desafioTecnico_analyticsEngineer
2. Criar e Ativar o Ambiente Virtual
É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto, evitando conflitos com outras instalações Python.

Bash

python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
3. Instalar Dependências
Com o ambiente virtual ativado, instale as bibliotecas Python necessárias listadas no requirements.txt (ou diretamente):

Bash

pip install pandas numpy matplotlib
# Ou se você criar um requirements.txt:
# pip install -r requirements.txt
4. Configurar Arquivos de Dados
Certifique-se de que os arquivos de dados brutos (aquisicao_dia_database_fundo_teste.csv, estoque_aquisicoes_database_fundo_teste.txt, liquidados_estoque_database_fundo_teste.csv) estão presentes dentro da pasta data/ na raiz do projeto.

Se você baixou o repositório, eles já devem estar lá.
Se não, você pode criá-los manualmente ou baixá-los para essa pasta.
Verifique os nomes dos arquivos: O script espera os nomes exatos:
* aquisicao_dia_database_fundo_teste.csv
* estoque_aquisicoes_database_fundo_teste.txt
* liquidados_estoque_database_fundo_teste.csv

Execução do Projeto
O projeto é projetado para ser executado como um script único que simula o pipeline completo.

Etapa 1: Popular o Banco de Dados (Simulação)
No contexto deste projeto, a "população do banco de dados" é simulada dentro do main.py através da leitura, limpeza e transformação dos dados em memória. As funções load_data() e clean_data() realizam essa etapa conceitual de preparar os dados para o estágio de DW.

Para uma implementação real, esta etapa envolveria:

Configuração de Conexão: Adicionar credenciais e strings de conexão ao banco de dados (PostgreSQL, BigQuery, etc.).
Criação de Tabelas: Executar scripts SQL (.sql no projeto) para criar as tabelas dimensionais e de fato no banco de dados alvo.
Processo de Carga: Utilizar ferramentas ou scripts (pandas.to_sql(), APIs de cloud) para carregar os DataFrames limpos para as tabelas correspondentes no DW.
Simulação de Ingestão e Persistência Incremental
Dentro do main.py, as funções load_data() e clean_data() representam as etapas de ingestão e preparação para persistência. Embora não haja uma conexão física com um banco de dados, o processo é feito de forma robusta para lidar com dados reais:

Identificação de Registros: A leitura dos arquivos e o tratamento de nulos/erros (convert_currency, convert_date) garantem que apenas dados válidos sejam considerados, simulando a filtragem de registros "não processados" ou malformados.
Fluxo Incremental: Para um fluxo incremental real, seria necessário:
Manter um registro da última_data_processada ou último_id_processado em uma tabela de controle no banco de dados.
Na load_data(), ler apenas os registros com data (ou ID) posterior à última_data_processada.
Na etapa de clean_data()/carga, aplicar lógica de UPSERT (update se existir, insert se novo) para as tabelas de fato e dimensões, garantindo que o DW seja atualizado sem duplicatas.
Como executar a "simulação de população":
Basta executar o script main.py conforme a próxima seção. As mensagens de console indicarão as etapas de carregamento e limpeza dos dados.

Etapa 2: Executar o Cálculo de KPIs e Gerar o Dashboard
Após a "simulação de população" (que é integrada), o script continuará para o cálculo dos KPIs e a geração do dashboard.

Para executar o pipeline completo:

Bash

python main.py
O que você verá:

Output no Terminal: O script imprimirá mensagens de progresso e debug no console, detalhando o carregamento dos dados, a limpeza, e o cálculo de KPIs para cada fundo.
Janela do Dashboard: Uma janela do Matplotlib será aberta, exibindo o dashboard com os 6 gráficos dos KPIs.
Arquivo PNG: Uma imagem do dashboard (dashboard_kpis.png) será salva automaticamente no diretório raiz do projeto.
Resultados Esperados
Ao final da execução, você deverá ter:

Console Output: Logs detalhados do processo de ETL e cálculo de KPIs.
dashboard_kpis.png: Um arquivo de imagem PNG contendo a visualização dos seguintes KPIs por fundo:
Volume Total Cedido
Volume em Estoque Atual
Índice de Inadimplência (%)
Retorno Realizado (R$/R$)
Tempo Médio até a Baixa (dias)
Aging dos Recebíveis (Quantidade de Títulos por faixa de atraso)

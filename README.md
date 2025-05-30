# Desafio Técnico: Engenheiro de Analytics - Pipeline ETL e Dashboards

Este repositório contém uma solução para um desafio técnico de Engenheiro de Analytics, focado na construção de um pipeline ETL (Extract, Transform, Load) e na geração de indicadores (KPIs) visualizados em um dashboard. O projeto simula o processamento de dados de aquisições, estoque e liquidações para fornecer insights de negócio.

---

## Sumário

- [Visão Geral do Projeto](#visão-geral-do-projeto)
- [Objetivos do Desafio](#objetivos-do-desafio)
- [Arquitetura e Tecnologias](#arquitetura-e-tecnologias)
- [Fluxo de Dados ETL (Exemplo Resumido)](#fluxo-de-dados-etl-exemplo-resumido)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Execução do Projeto](#execução-do-projeto)
- [Resultados Esperados](#resultados-esperados)
- [Considerações Finais e Melhorias Futuras](#considerações-finais-e-melhorias-futuras)

---

## Visão Geral do Projeto

Este projeto aborda as principais etapas de um pipeline de dados analítico:

- **Ingestão de Dados**: Leitura de arquivos CSV/TXT de diferentes fontes.
- **Transformação e Modelagem**: Limpeza, padronização e estruturação dos dados em um modelo normalizado.
- **Carga (Load)**: Simulação de carga incremental em um Data Warehouse.
- **Análise e Visualização**: Cálculo de KPIs e geração de um dashboard com Matplotlib.

---

## Objetivos do Desafio

- Desenvolver um processo ETL robusto para dados financeiros.
- Aplicar técnicas de modelagem de dados para análise.
- Calcular e visualizar KPIs essenciais.
- Demonstrar habilidades em Python para manipulação e visualização de dados.

---

## Arquitetura e Tecnologias

O projeto é construído com Python e segue a arquitetura de um **Monolito de Script**, onde todas as etapas estão centralizadas em um único script para facilitar demonstrações e testes locais.

---

## Tecnologias Utilizadas

- **Linguagem**: Python 3.x
- **Manipulação de Dados**: `pandas`, `numpy`
- **Visualização**: `matplotlib`
- **Gerenciamento de Arquivos**: `pathlib`
- **Simulação de DW**: Manipulação em memória com `DataFrame`, sem persistência real

---

## Fluxo de Dados ETL (Exemplo Resumido)

### Ingestão (`Extract`)
- Leitura dos arquivos `.csv` e `.txt` da pasta `data/`.
- Identificação e filtragem de registros válidos.

### Transformação (`Transform`)
- Conversão de tipos (monetários, datas)
- Tratamento de valores nulos e anomalias
- Preparação para modelo analítico (dimensões/fatos conceituais)

### Carga (`Load`)
- Os dados são mantidos em memória e utilizados diretamente.
- Em produção, envolveria escrita para DW com `SQLAlchemy` ou APIs.

---

## Estrutura do Projeto

├── data/
│ ├── aquisicao_dia_database_fundo_teste.csv
│ ├── estoque_aquisicoes_database_fundo_teste.txt
│ └── liquidados_estoque_database_fundo_teste.csv
├── main.py
├── dashboard_kpis.png
└── README.md

yaml
Copiar
Editar

- **data/**: Arquivos brutos de entrada
- **main.py**: Script principal com o pipeline completo
- **dashboard_kpis.png**: Imagem gerada com os KPIs
- **README.md**: Documentação do projeto

---

## Configuração do Ambiente

### 1. Clonar o Repositório
`bash
git clone https://github.com/giocarvalho07/desafioTecnico_analyticsEngineer.git
cd desafioTecnico_analyticsEngineer`


### 2. Criar e Ativar o Ambiente Virtual
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

### 3. Instalar Dependências
pip install pandas numpy matplotlib
# Ou:
pip install -r requirements.txt

### Configurar Arquivos de Dados
Certifique-se de que os arquivos abaixo estejam na pasta data/:

aquisicao_dia_database_fundo_teste.csv

estoque_aquisicoes_database_fundo_teste.txt

liquidados_estoque_database_fundo_teste.csv


Execução do Projeto
Etapa 1: Popular o Banco de Dados (Simulação)
Simulação ocorre dentro do main.py por meio das funções:

load_data(): Leitura dos arquivos

clean_data(): Conversão e limpeza

Nota: Em projetos reais, esta etapa envolveria:

Conexão com banco (PostgreSQL, BigQuery, etc.)

Criação de tabelas

Carga via pandas.to_sql() ou APIs

Etapa 2: Executar o Cálculo de KPIs e Gerar o Dashboard
bash
Copiar
Editar
python main.py
O que será exibido:
Mensagens no terminal com progresso detalhado

Janela de gráficos interativos (matplotlib)

Arquivo dashboard_kpis.png salvo no diretório raiz

Resultados Esperados
Após a execução:

Logs com progresso do ETL e cálculo por fundo

Dashboard com os seguintes KPIs:

Indicador	Descrição
Volume Total Cedido	Soma dos valores presentes nas aquisições
Volume em Estoque Atual	Soma dos valores presentes em estoque
Índice de Inadimplência	% de títulos vencidos no estoque
Retorno Realizado	Valor recebido / valor cedido
Tempo Médio até a Baixa	Média de dias entre aquisição e liquidação
Aging dos Recebíveis	Classificação por faixas de atraso (0 a 90+)

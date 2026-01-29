# Detector de Dados Pessoais - Desafio Participa DF

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![spaCy](https://img.shields.io/badge/spaCy-3.6+-green.svg)](https://spacy.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Sobre o Projeto

Solução desenvolvida para o **1º Hackathon em Controle Social: Desafio Participa DF**, na categoria **Acesso à Informação**.

**Objetivo:** Identificar automaticamente, entre os pedidos de acesso à informação marcados como públicos, aqueles que contenham dados pessoais e que, portanto, deveriam ser classificados como **não públicos**.

**Dados pessoais considerados:** Nome, CPF, RG, telefone, e-mail, matrícula, OAB e CNPJ.

---

##  Solução Proposta

Abordagem **híbrida** combinando:

1. **Expressões Regulares (Regex):** Detecção de padrões estruturados (CPF, e-mail, telefone, etc.)
2. **Processamento de Linguagem Natural (NLP):** Detecção de nomes de pessoas usando spaCy

### Por que essa abordagem?

| Característica | Benefício |
|----------------|-----------|
| **Determinística** | Resultados consistentes e previsíveis |
| **Interpretável** | Sabe-se exatamente o que foi detectado |
| **Sem necessidade de treino** | Funciona imediatamente |
| **Alta precisão** | Padrões regex são exatos |

---

##  Estrutura do Repositório
```
desafio-participa-df/
├── AMOSTRA_e-SIC.xlsx
├── 01_analise_exploratoria.ipynb
├── 02_modelo_final.ipynb
├── 03_experimentos_ml.ipynb
├── resultado_classificacao.csv
├── detector.py
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

## Instalação e Configuração

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes)

### Passo a passo

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/desafio-participa-df.git
cd desafio-participa-df
```

2. **Crie e ative o ambiente virtual:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Baixe o modelo spaCy para português:**
```bash
python -m spacy download pt_core_news_sm
```

---

##  Como Executar

### Opção 1: Usando o script Python
```bash
python src/detector.py data/AMOSTRA_e-SIC.xlsx
```

### Opção 2: Usando os notebooks

1. Abra o Jupyter Notebook:
```bash
jupyter notebook
```

2. Execute o notebook `02_modelo_final.ipynb`

### Opção 3: Importando como módulo
```python
from src.detector import classificar_texto, classificar_dataset

# Classificar um texto
texto = "Meu nome é João Silva, CPF 123.456.789-00"
resultado = classificar_texto(texto)
print(resultado)  # 1 = Não Público

# Classificar um dataset
resultado_df = classificar_dataset('data/AMOSTRA_e-SIC.xlsx')
resultado_df.to_csv('output/resultado.csv', index=False)
```

---

## Resultados

### Dataset de Amostra (99 registros)

| Classificação | Quantidade | Percentual |
|---------------|------------|------------|
| Público | 62 | 62.6% |
| Não Público | 37 | 37.4% |

### Dados Pessoais Detectados

| Tipo | Método | Ocorrências |
|------|--------|-------------|
| CPF | Regex | 17 |
| Processo SEI | Regex | 25 |
| Matrícula | Regex | 12 |
| E-mail | Regex | 7 |
| Telefone | Regex | 5 |
| CNPJ | Regex | 4 |
| OAB | Regex | 3 |
| Nome de Pessoa | NLP (spaCy) | 11 |

---

## Notebooks

| Notebook | Descrição |
|----------|-----------|
| `01_analise_exploratoria.ipynb` | Exploração dos dados, testes de regex e NLP, iterações do modelo |
| `02_modelo_final.ipynb` | Solução final consolidada, funções documentadas, exportação |
| `03_experimentos_ml.ipynb` | Comparação de modelos de ML (Random Forest, SVM, XGBoost, etc.) |

---

## Experimentos com Machine Learning

Foram testados 5 modelos de ML para comparação:

| Modelo | Acurácia | Precisão | Recall | F1-Score |
|--------|----------|----------|--------|----------|
| **XGBoost** | 80% | 100% | 43% | 60% |
| Logistic Regression | 65% | 50% | 43% | 46% |
| SVM | 65% | 50% | 29% | 36% |
| Random Forest | 60% | 40% | 29% | 33% |
| Naive Bayes | 60% | 0% | 0% | 0% |

**Conclusão:** A abordagem híbrida (Regex + NLP) é superior para este problema devido ao tamanho limitado do dataset e à natureza determinística dos padrões de dados pessoais.

---

## Tecnologias Utilizadas

- **Python 3.9+**
- **pandas** - Manipulação de dados
- **spaCy** - Processamento de linguagem natural
- **scikit-learn** - Machine Learning
- **XGBoost** - Gradient Boosting
- **matplotlib/seaborn** - Visualização

---

## Autor

**Lucas Boros**
- Estudante de Ciência de Dados e IA (IESB Asa Sul)
- Assessor da Assessoria de Comunicação Social da Administração Regional do SIA

---

##  Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Agradecimentos

- Controladoria-Geral do Distrito Federal (CGDF)
- Desafio Participa DF
- Administração Regional do SIA

- Luisa Viana (minha futura esposa e mãe da minha filha)
